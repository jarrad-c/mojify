from features import FEATURES

GENDERS = [["male", 1], ["female", 2]]

OUTFIT = 889223

basePreviewUrl = "https://preview.bitmoji.com/avatar-builder-v3/preview/"


def mapTraits(traits):
    map=''
    for key in traits.keys():
        map=f"{map}&{key}={traits[key]}"
    return map


def buildPreviewUrl(traits):
    trait_string = mapTraits(traits)
    url = f"{basePreviewUrl}head?scale=1&style=5&rotation=0{trait_string}&outfit={OUTFIT}"
    return url


def createFromFeatures(features):
    traits = {}
    for feature in features:
        if (feature in FEATURES.keys()) and (feature != 'Sideburns'):
            key = FEATURES[feature]['trait']
            value = FEATURES[feature]['value']
            traits[key] = value

    if 'Male' not in features:
        traits['gender'] = 2
        if 'Straight_Hair' in features:
            if 'Bangs' in features:
                traits['hair'] = 1313
            else:
                traits['hair'] = 1314
        elif 'Wavy_Hair' in features:
            if 'Bangs' in features:
                traits['hair'] = 1319
            else:
                traits['hair'] = 1321

    if 'Pale_Skin' not in features:
        traits['skin_tone'] = 14664067

    if 'Young' not in features:
        traits['face_lines'] = 1366

    if 'Wearing_Lipstick' not in features:
        traits['lipstick_tone'] = 12941689

    if ('Big_Nose' in features) and ('Pointy_Nose' in features):
        traits['nose'] = 1489

    if ('Goatee' in features) and ('Mustache' in features):
        if 'Sideburns' in features:
            traits['beard'] = 1343
        else:
            traits['beard'] = 2321
    elif('Goatee' in features) and ('Sideburns' in features):
        traits['beard'] = 1343
    elif ('Mustache' in features) and ('5_o_clock_shadow' in features):
        traits['beard'] = 2253

    if('Sideburns' in features) and ('beard' not in traits.keys()):
        traits['beard'] = FEATURES['Sideburns']

    return buildPreviewUrl(traits)
