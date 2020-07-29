"""Script to convert the Diffuse Flux contour to a format where it can be
plotted as a 'butterfly contour'.

The values are taken from https://arxiv.org/pdf/1507.03991, tracing the 68%
and 95% contours in Figure 1.

C
"""
import numpy as np
from astropy import units as u

contour_68 = [
    (2.362728669872589, 6.014203559565713),
    (2.362693966585692, 5.8056368053145615),
    (2.363985424619503, 5.567299588518169),
    (2.365274403847107, 5.314064746418125),
    (2.371907689256854, 5.180110058995587),
    (2.3798720935997224, 5.04618015963512),
    (2.3905036934212482, 4.942095087006098),
    (2.401135293242774, 4.838010014377076),
    (2.4144390461553713, 4.793565019086808),
    (2.4277551930990033, 4.823608150314808),
    (2.5569555302166473, 5.3176342273561055),
    (2.5742774279906797, 5.422239849288582),
    (2.587615884190174, 5.586361608249467),
    (2.5996232214565462, 5.750458579148281),
    (2.6143051906201973, 5.989093252689504),
    (2.6263274007238113, 6.242575975410243),
    (2.635699766992216, 6.57049724852511),
    (2.637080462049477, 6.8684745426602545),
    (2.6331342025680433, 7.151455059243469),
    (2.6265182688017448, 7.389693123791582),
    (2.617245054781617, 7.657676862822864),
    (2.6066308066035395, 7.866045312577462),
    (2.586711119924644, 8.148728372415844),
    (2.565442962669178, 8.32710326706658),
    (2.5508105696296663, 8.386421099598433),
    (2.528191462991423, 8.44559020375787),
    (2.501561647910366, 8.400401566605522),
    (2.477581676664518, 8.280774379059045),
    (2.456254028060086, 8.10160626642209),
    (2.441577016508849, 7.892766843488175),
    (2.4242476823161963, 7.743468345644738),
    (2.4148951464974466, 7.5347280749591),
    (2.3895245649695105, 7.0575330920628625),
    (2.3788186009617767, 6.714689405582271),
    (2.370787268851321, 6.4463834217440885),
    (2.3680928065043876, 6.2526647166724505),
]

contour_95 = [
    (2.534660033167496, 9.597014925373134),
    (2.5014925373134327, 9.53731343283582),
    (2.4723051409618573, 9.373134328358208),
    (2.445771144278607, 9.164179104477611),
    (2.4165837479270316, 8.880597014925373),
    (2.398009950248756, 8.611940298507463),
    (2.3728026533996682, 8.26865671641791),
    (2.3529021558872305, 7.865671641791044),
    (2.333001658374793, 7.44776119402985),
    (2.3144278606965174, 6.970149253731343),
    (2.295854063018242, 6.507462686567164),
    (2.2812603648424545, 5.999999999999999),
    (2.2693200663349917, 5.641791044776119),
    (2.2587064676616917, 5.253731343283581),
    (2.2480928689883912, 4.91044776119403),
    (2.2454394693200666, 4.567164179104477),
    (2.246766169154229, 4.134328358208956),
    (2.2640132669983415, 3.776119402985075),
    (2.298507462686567, 3.5820895522388057),
    (2.334328358208955, 3.5373134328358207),
    (2.3648424543946933, 3.5522388059701493),
    (2.3860696517412934, 3.5522388059701493),
    (2.417910447761194, 3.611940298507462),
    (2.431177446102819, 3.6716417910447765),
    (2.569154228855721, 4.17910447761194),
    (2.599668325041459, 4.388059701492536),
    (2.627529021558872, 4.6268656716417915),
    (2.6514096185737976, 4.895522388059701),
    (2.677943615257048, 5.2835820895522385),
    (2.701824212271973, 5.791044776119403),
    (2.7124378109452736, 6.313432835820896),
    (2.711111111111111, 6.9402985074626855),
    (2.699170812603648, 7.701492537313433),
    (2.676616915422885, 8.26865671641791),
    (2.6474295190713097, 8.865671641791044),
    (2.619568822553897, 9.17910447761194),
    (2.594361525704809, 9.402985074626866),
    (2.5678275290215584, 9.53731343283582),
]

# Convert from all-flavour to muon-neutrino flux

units = 10 ** -18 / 3. #/ u.GeV /u.cm**2 / u.s / u.sr

# IceCube Joint Best Fit
# (https://arxiv.org/abs/1507.03991)
#all-flabour to muon only
best_fit_flux = 6.7 * units * (
        u.GeV ** -1 * u.cm ** -2 * u.s ** -1 * u.sr ** -1
)
best_fit_gamma = 2.5

# Fit is valid from 25 TeV to 2.8 PeV
e_range = np.logspace(np.log10(25) + 3, np.log10(2.8) + 6, 100)

joint_15 = {
    "joint_15": (best_fit_flux, best_fit_gamma, np.array(contour_68)*units, np.array(contour_95)*units, e_range)
}

