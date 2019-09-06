"""Script to calculate the sensitivity and discovery potential for different

"""
from builtins import str
import numpy as np
from flarestack.core.results import ResultsHandler
from flarestack.data.icecube import ps_v002_p01
from flarestack.shared import plot_output_dir, flux_to_k, make_analysis_pickle
from flarestack.icecube_utils.reference_sensitivity import reference_sensitivity
from flarestack.analyses.ccsn.shared_ccsn import sn_cats, sn_catalogue_name, \
    sn_time_pdfs
from flarestack.cluster import run_desy_cluster as rd
import math
import matplotlib.pyplot as plt
from flarestack.utils.custom_seasons import custom_dataset
import os
from flarestack.core.minimisation import MinimisationHandler

analyses = dict()

# Initialise Injectors/LLHs

llh_energy = {
    "Name": "Power Law",
}

gammas = [1.8, 1.9, 2.0, 2.1, 2.3, 2.5, 2.7]
# gammas = [1.8, 2.0, 2.5]
# gamma = [2.0]
raw = "analyses/ccsn/calculate_sensitivity/"

full_res = dict()

for cat in sn_cats:

    name = raw + cat + "/"

    cat_path = sn_catalogue_name(cat)
    catalogue = np.load(cat_path)

    closest_src = np.sort(catalogue, order="Distance (Mpc)")[0]

    cat_res = dict()

    time_pdfs = sn_time_pdfs(cat)

    for llh_time in time_pdfs:

        time_key = str(llh_time["Post-Window"] + llh_time["Pre-Window"])

        time_name = name + time_key + "/"

        time_res = dict()

        for i, fit_weights in enumerate([False, True]):

            res = dict()

            mh_name = ["fixed_weights", "fit_weights"][i]

            l_name = time_name + mh_name + "/"

            llh_kwargs = {
                "name": "standard",
                "LLH Energy PDF": llh_energy,
                "LLH Time PDF": llh_time,
            }

            injection_time = llh_time

            for gamma in gammas:

                full_name = l_name + str(gamma) + "/"

                length = float(time_key)

                scale = (flux_to_k(reference_sensitivity(
                    np.sin(closest_src["dec"]), gamma=gamma
                ) * 40 * math.sqrt(float(len(catalogue)))) * 200.) / length

                injection_energy = dict(llh_energy)
                injection_energy["Gamma"] = gamma

                inj_kwargs = {
                    "Injection Energy PDF": injection_energy,
                    "Injection Time PDF": injection_time,
                    "Poisson Smear?": True,
                }

                mh_dict = {
                    "name": full_name,
                    "mh_name": "standard",
                    "datasets": custom_dataset(ps_v002_p01, catalogue,
                                               llh_kwargs["LLH Time PDF"]),
                    "catalogue": cat_path,
                    "inj kwargs": inj_kwargs,
                    "llh_dict": llh_kwargs,
                    "scale": scale,
                    "n_trials": 5,
                    "n_steps": 20
                }

                pkl_file = make_analysis_pickle(mh_dict)

                # rd.submit_to_cluster(pkl_file, n_jobs=50)

                mh = MinimisationHandler(mh_dict)
                mh.iterate_run(mh_dict["scale"], mh_dict["n_steps"],
                               n_trials=1)

                res[gamma] = mh_dict

            time_res[mh_name] = res

        cat_res[time_key] = time_res

    full_res[cat] = cat_res

rd.wait_for_cluster()

for b, (cat_name, cat_res) in enumerate(full_res.items()):

    for (time_key, time_res) in cat_res.items():

        for (mh_name, src_res) in time_res.items():

            sens_livetime = []
            fracs = []
            disc_pots_livetime = []
            sens_e = []
            disc_e = []

            labels = []

            for (gamma, rh_dict) in sorted(src_res.items()):

                rh = ResultsHandler(rh_dict)

                inj = rh_dict["inj kwargs"]["Injection Time PDF"]
                injection_length = inj["Pre-Window"] + inj["Post-Window"]

                inj_time = injection_length * 60 * 60 * 24

                astro_sens, astro_disc = rh.astro_values(
                    rh_dict["inj kwargs"]["Injection Energy PDF"])

                key = "Total Fluence (GeV cm^{-2} s^{-1})"

                e_key = "Mean Luminosity (erg/s)"

                sens_livetime.append(astro_sens[key] * inj_time)
                disc_pots_livetime.append(astro_disc[key] * inj_time)

                sens_e.append(astro_sens[e_key] * inj_time)
                disc_e.append(astro_disc[e_key] * inj_time)

                fracs.append(gamma)


                # plt.plot(fracs, disc_pots, linestyle="--", color=cols[i])

            name = os.path.dirname(src_res.itervalues.__next()["name"][:-1])

            for j, [fluence, energy] in enumerate([[sens_livetime, sens_e],
                                                  [disc_pots_livetime, disc_e]]):

                plt.figure()
                ax1 = plt.subplot(111)

                ax2 = ax1.twinx()

                # cols = ["#00A6EB", "#F79646", "g", "r"]
                linestyle = ["-", "-"][j]

                ax1.plot(fracs, fluence, label=labels, linestyle=linestyle,
                         )
                ax2.plot(fracs, energy, linestyle=linestyle,
                         )

                y_label = [r"Total Fluence [GeV cm$^{-2}$]",
                           r"Mean Isotropic-Equivalent $E_{\nu}$ (erg)"]

                ax2.grid(True, which='both')
                ax1.set_ylabel(r"Total Fluence [GeV cm$^{-2}$]", fontsize=12)
                ax2.set_ylabel(r"Mean Isotropic-Equivalent $E_{\nu}$ (erg)")
                ax1.set_xlabel(r"Spectral Index ($\gamma$)")
                ax1.set_yscale("log")
                ax2.set_yscale("log")

                for k, ax in enumerate([ax1, ax2]):
                    y = [fluence, energy][k]

                    ax.set_ylim(0.95 * min(y),
                                1.1 * max(y))

                plt.title("Stacked " + ["Sensitivity", "Discovery Potential"][j] +
                          " for " + cat_name + " SNe")

                plt.tight_layout()
                plt.savefig(plot_output_dir(name) + "/spectral_index_" +
                            ["sens", "disc"][j] + "_" + cat_name + ".pdf")
                plt.close()

