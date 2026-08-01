# Security Events

## V16.3.1

Verify that all authentication operations are logged, including successful and unsuccessful attempts. Additional metadata, such as the type of authentication or factors used, should also be collected.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [114](/taxonomy/capec-3.9/114), [151](/taxonomy/capec-3.9/151), [156](/taxonomy/capec-3.9/156), [2](/taxonomy/capec-3.9/2), [206](/taxonomy/capec-3.9/206), [21](/taxonomy/capec-3.9/21), [268](/taxonomy/capec-3.9/268), [39](/taxonomy/capec-3.9/39), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50), [600](/taxonomy/capec-3.9/600), [68](/taxonomy/capec-3.9/68), [70](/taxonomy/capec-3.9/70), [75](/taxonomy/capec-3.9/75)

## V16.3.2

Verify that failed authorization attempts are logged. For L3, this must include logging all authorization decisions, including logging when sensitive data is accessed (without logging the sensitive data itself).

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1), [11](/taxonomy/capec-3.9/11), [114](/taxonomy/capec-3.9/114), [116](/taxonomy/capec-3.9/116), [121](/taxonomy/capec-3.9/121), [122](/taxonomy/capec-3.9/122), [126](/taxonomy/capec-3.9/126), [133](/taxonomy/capec-3.9/133), [143](/taxonomy/capec-3.9/143), [144](/taxonomy/capec-3.9/144), [149](/taxonomy/capec-3.9/149), [151](/taxonomy/capec-3.9/151), [155](/taxonomy/capec-3.9/155), [156](/taxonomy/capec-3.9/156), [162](/taxonomy/capec-3.9/162), [166](/taxonomy/capec-3.9/166), [172](/taxonomy/capec-3.9/172), [176](/taxonomy/capec-3.9/176), [179](/taxonomy/capec-3.9/179), [180](/taxonomy/capec-3.9/180), [203](/taxonomy/capec-3.9/203), [206](/taxonomy/capec-3.9/206), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [212](/taxonomy/capec-3.9/212), [22](/taxonomy/capec-3.9/22), [240](/taxonomy/capec-3.9/240), [268](/taxonomy/capec-3.9/268), [36](/taxonomy/capec-3.9/36), [39](/taxonomy/capec-3.9/39), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50), [54](/taxonomy/capec-3.9/54), [58](/taxonomy/capec-3.9/58), [600](/taxonomy/capec-3.9/600), [68](/taxonomy/capec-3.9/68), [74](/taxonomy/capec-3.9/74), [75](/taxonomy/capec-3.9/75), [87](/taxonomy/capec-3.9/87), [95](/taxonomy/capec-3.9/95)

## V16.3.3

Verify that the application logs the security events that are defined in the documentation and also logs attempts to bypass the security controls, such as input validation, business logic, and anti-automation.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [1](/taxonomy/capec-3.9/1), [100](/taxonomy/capec-3.9/100), [105](/taxonomy/capec-3.9/105), [11](/taxonomy/capec-3.9/11), [112](/taxonomy/capec-3.9/112), [113](/taxonomy/capec-3.9/113), [114](/taxonomy/capec-3.9/114), [115](/taxonomy/capec-3.9/115), [116](/taxonomy/capec-3.9/116), [121](/taxonomy/capec-3.9/121), [122](/taxonomy/capec-3.9/122), [125](/taxonomy/capec-3.9/125), [126](/taxonomy/capec-3.9/126), [127](/taxonomy/capec-3.9/127), [130](/taxonomy/capec-3.9/130), [133](/taxonomy/capec-3.9/133), [136](/taxonomy/capec-3.9/136), [137](/taxonomy/capec-3.9/137), [140](/taxonomy/capec-3.9/140), [145](/taxonomy/capec-3.9/145), [151](/taxonomy/capec-3.9/151), [152](/taxonomy/capec-3.9/152), [153](/taxonomy/capec-3.9/153), [155](/taxonomy/capec-3.9/155), [156](/taxonomy/capec-3.9/156), [157](/taxonomy/capec-3.9/157), [160](/taxonomy/capec-3.9/160), [162](/taxonomy/capec-3.9/162), [165](/taxonomy/capec-3.9/165), [166](/taxonomy/capec-3.9/166), [172](/taxonomy/capec-3.9/172), [175](/taxonomy/capec-3.9/175), [176](/taxonomy/capec-3.9/176), [179](/taxonomy/capec-3.9/179), [180](/taxonomy/capec-3.9/180), [183](/taxonomy/capec-3.9/183), [184](/taxonomy/capec-3.9/184), [188](/taxonomy/capec-3.9/188), [19](/taxonomy/capec-3.9/19), [198](/taxonomy/capec-3.9/198), [2](/taxonomy/capec-3.9/2), [20](/taxonomy/capec-3.9/20), [201](/taxonomy/capec-3.9/201), [204](/taxonomy/capec-3.9/204), [206](/taxonomy/capec-3.9/206), [207](/taxonomy/capec-3.9/207), [21](/taxonomy/capec-3.9/21), [212](/taxonomy/capec-3.9/212), [216](/taxonomy/capec-3.9/216), [217](/taxonomy/capec-3.9/217), [218](/taxonomy/capec-3.9/218), [22](/taxonomy/capec-3.9/22), [220](/taxonomy/capec-3.9/220), [227](/taxonomy/capec-3.9/227), [23](/taxonomy/capec-3.9/23), [231](/taxonomy/capec-3.9/231), [233](/taxonomy/capec-3.9/233), [234](/taxonomy/capec-3.9/234), [24](/taxonomy/capec-3.9/24), [240](/taxonomy/capec-3.9/240), [242](/taxonomy/capec-3.9/242), [248](/taxonomy/capec-3.9/248), [25](/taxonomy/capec-3.9/25), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [26](/taxonomy/capec-3.9/26), [261](/taxonomy/capec-3.9/261), [267](/taxonomy/capec-3.9/267), [268](/taxonomy/capec-3.9/268), [272](/taxonomy/capec-3.9/272), [28](/taxonomy/capec-3.9/28), [30](/taxonomy/capec-3.9/30), [33](/taxonomy/capec-3.9/33), [36](/taxonomy/capec-3.9/36), [37](/taxonomy/capec-3.9/37), [383](/taxonomy/capec-3.9/383), [39](/taxonomy/capec-3.9/39), [43](/taxonomy/capec-3.9/43), [441](/taxonomy/capec-3.9/441), [444](/taxonomy/capec-3.9/444), [461](/taxonomy/capec-3.9/461), [463](/taxonomy/capec-3.9/463), [469](/taxonomy/capec-3.9/469), [473](/taxonomy/capec-3.9/473), [474](/taxonomy/capec-3.9/474), [475](/taxonomy/capec-3.9/475), [48](/taxonomy/capec-3.9/48), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50), [523](/taxonomy/capec-3.9/523), [54](/taxonomy/capec-3.9/54), [549](/taxonomy/capec-3.9/549), [554](/taxonomy/capec-3.9/554), [57](/taxonomy/capec-3.9/57), [572](/taxonomy/capec-3.9/572), [586](/taxonomy/capec-3.9/586), [594](/taxonomy/capec-3.9/594), [600](/taxonomy/capec-3.9/600), [603](/taxonomy/capec-3.9/603), [607](/taxonomy/capec-3.9/607), [620](/taxonomy/capec-3.9/620), [633](/taxonomy/capec-3.9/633), [636](/taxonomy/capec-3.9/636), [639](/taxonomy/capec-3.9/639), [64](/taxonomy/capec-3.9/64), [66](/taxonomy/capec-3.9/66), [664](/taxonomy/capec-3.9/664), [676](/taxonomy/capec-3.9/676), [68](/taxonomy/capec-3.9/68), [69](/taxonomy/capec-3.9/69), [70](/taxonomy/capec-3.9/70), [74](/taxonomy/capec-3.9/74), [75](/taxonomy/capec-3.9/75), [77](/taxonomy/capec-3.9/77), [83](/taxonomy/capec-3.9/83), [88](/taxonomy/capec-3.9/88), [93](/taxonomy/capec-3.9/93), [94](/taxonomy/capec-3.9/94), [95](/taxonomy/capec-3.9/95), [97](/taxonomy/capec-3.9/97)

## V16.3.4

Verify that the application logs unexpected errors and security control failures such as backend TLS failures.

Required for Level 2 and 3

### Related CAPEC™ Requirements

CAPEC™ (3.9): [105](/taxonomy/capec-3.9/105), [114](/taxonomy/capec-3.9/114), [136](/taxonomy/capec-3.9/136), [145](/taxonomy/capec-3.9/145), [151](/taxonomy/capec-3.9/151), [156](/taxonomy/capec-3.9/156), [157](/taxonomy/capec-3.9/157), [159](/taxonomy/capec-3.9/159), [160](/taxonomy/capec-3.9/160), [169](/taxonomy/capec-3.9/169), [175](/taxonomy/capec-3.9/175), [176](/taxonomy/capec-3.9/176), [183](/taxonomy/capec-3.9/183), [184](/taxonomy/capec-3.9/184), [19](/taxonomy/capec-3.9/19), [201](/taxonomy/capec-3.9/201), [206](/taxonomy/capec-3.9/206), [21](/taxonomy/capec-3.9/21), [216](/taxonomy/capec-3.9/216), [217](/taxonomy/capec-3.9/217), [218](/taxonomy/capec-3.9/218), [220](/taxonomy/capec-3.9/220), [23](/taxonomy/capec-3.9/23), [24](/taxonomy/capec-3.9/24), [250](/taxonomy/capec-3.9/250), [253](/taxonomy/capec-3.9/253), [268](/taxonomy/capec-3.9/268), [272](/taxonomy/capec-3.9/272), [310](/taxonomy/capec-3.9/310), [33](/taxonomy/capec-3.9/33), [39](/taxonomy/capec-3.9/39), [438](/taxonomy/capec-3.9/438), [442](/taxonomy/capec-3.9/442), [445](/taxonomy/capec-3.9/445), [446](/taxonomy/capec-3.9/446), [461](/taxonomy/capec-3.9/461), [475](/taxonomy/capec-3.9/475), [49](/taxonomy/capec-3.9/49), [50](/taxonomy/capec-3.9/50), [511](/taxonomy/capec-3.9/511), [523](/taxonomy/capec-3.9/523), [538](/taxonomy/capec-3.9/538), [594](/taxonomy/capec-3.9/594), [600](/taxonomy/capec-3.9/600), [620](/taxonomy/capec-3.9/620), [633](/taxonomy/capec-3.9/633), [636](/taxonomy/capec-3.9/636), [66](/taxonomy/capec-3.9/66), [664](/taxonomy/capec-3.9/664), [673](/taxonomy/capec-3.9/673), [68](/taxonomy/capec-3.9/68), [690](/taxonomy/capec-3.9/690), [691](/taxonomy/capec-3.9/691), [83](/taxonomy/capec-3.9/83), [94](/taxonomy/capec-3.9/94)

## Disclaimer

Credit via [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).For more information visit: [The OWASP ASVS Project](https://owasp.org/www-project-application-security-verification-standard/) or [Github respository.](https://github.com/OWASP/ASVS). OWASP ASVS is under the [Creative Commons Attribution-Share Alike v4.0](https://github.com/OWASP/ASVS/blob/v5.0.0/LICENSE.md) license.
