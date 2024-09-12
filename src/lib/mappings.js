let mappings = {
  "meta": {
    "edition": "webapp",
    "component": "mappings",
    "language": "ALL",
    "version": "1.22",
    "layouts": [
      "cards",
      "leaflet",
      "guide"
    ],
    "templates": [
      "bridge_qr",
      "bridge",
      "tarot",
      "tarot_qr"
    ],
    "languages": [
      "en",
      "es",
      "fr",
      "nl",
      "nl",
      "no-nb",
      "pt-br"
    ]
  },
  "suits": [
    {
      "id": "VE",
      "name": "DATA VALIDATION & ENCODING",
      "cards": [
        {
          "id": "VE2",
          "value": "2",
          "owasp_scp": [
            69,
            107,
            108,
            109,
            136,
            137,
            153,
            156,
            158,
            162
          ],
          "owasp_asvs": [
            "1.10",
            4.5,
            8.1,
            11.5,
            19.1,
            19.5
          ],
          "owasp_appsensor": [
            "HT1-3"
          ],
          "capec": [
            54,
            541
          ],
          "safecode": [
            4,
            23
          ]
        },
        {
          "id": "VE3",
          "value": "3",
          "owasp_scp": [],
          "owasp_asvs": [
            5.1,
            5.16,
            5.17,
            5.18,
            5.19,
            "5.20",
            11.1,
            11.2
          ],
          "owasp_appsensor": [
            "RE7-8",
            "AE4-7",
            "IE2-3",
            "CIE1",
            "CIE3-4",
            "HT1-3"
          ],
          "capec": [
            28,
            48,
            126,
            165,
            213,
            220,
            221,
            261,
            262,
            271,
            272
          ],
          "safecode": [
            3,
            16,
            24,
            35
          ]
        },
        {
          "id": "VE4",
          "value": "4",
          "owasp_scp": [
            8,
            10,
            183
          ],
          "owasp_asvs": [
            4.16,
            5.16,
            5.17,
            15.1
          ],
          "owasp_appsensor": [
            "RE3-6",
            "AE8-11",
            "SE1",
            "SE3-6",
            "IE2-4",
            "HT1-3"
          ],
          "capec": [
            28,
            31,
            48,
            126,
            162,
            165,
            213,
            220,
            221,
            261
          ],
          "safecode": [
            24,
            35
          ]
        },
        {
          "id": "VE5",
          "value": "5",
          "owasp_scp": [
            3,
            15,
            18,
            19,
            20,
            21,
            22,
            168
          ],
          "owasp_asvs": [
            1.7,
            5.15,
            5.21,
            5.22,
            5.23
          ],
          "owasp_appsensor": [],
          "capec": [
            28,
            31,
            152,
            160,
            468
          ],
          "safecode": [
            2,
            17
          ]
        },
        {
          "id": "VE6",
          "value": "6",
          "owasp_scp": [
            3,
            168
          ],
          "owasp_asvs": [
            1.7,
            5.6,
            5.19
          ],
          "owasp_appsensor": [
            "IE2-3"
          ],
          "capec": [
            28
          ],
          "safecode": [
            3,
            16,
            24
          ]
        },
        {
          "id": "VE7",
          "value": "7",
          "owasp_scp": [
            4,
            5,
            7,
            150
          ],
          "owasp_asvs": [
            5.6,
            11.8
          ],
          "owasp_appsensor": [
            "IE2-3",
            "EE1-2"
          ],
          "capec": [
            28,
            153,
            165
          ],
          "safecode": [
            3,
            16,
            24
          ]
        },
        {
          "id": "VE8",
          "value": "8",
          "owasp_scp": [
            15,
            169
          ],
          "owasp_asvs": [
            1.7,
            5.21,
            5.23
          ],
          "owasp_appsensor": [],
          "capec": [
            28,
            31,
            152,
            160,
            468
          ],
          "safecode": [
            2,
            17
          ]
        },
        {
          "id": "VE9",
          "value": "9",
          "owasp_scp": [
            6,
            21,
            22,
            168
          ],
          "owasp_asvs": [
            5.3
          ],
          "owasp_appsensor": [
            "IE2-3"
          ],
          "capec": [
            28
          ],
          "safecode": [
            3,
            16,
            24
          ]
        },
        {
          "id": "VEX",
          "value": "10",
          "owasp_scp": [
            2,
            19,
            92,
            95,
            180
          ],
          "owasp_asvs": [
            5.19,
            10.6,
            16.2,
            16.3,
            16.4,
            16.5,
            16.8
          ],
          "owasp_appsensor": [
            "IE4",
            "IE5"
          ],
          "capec": [
            12,
            51,
            57,
            90,
            111,
            145,
            194,
            195,
            202,
            218,
            463
          ],
          "safecode": [
            14
          ]
        },
        {
          "id": "VEJ",
          "value": "J",
          "owasp_scp": [
            1,
            17
          ],
          "owasp_asvs": [
            5.5,
            5.18
          ],
          "owasp_appsensor": [
            "RE3",
            "RE4"
          ],
          "capec": [
            87,
            207,
            554
          ],
          "safecode": [
            2,
            17
          ]
        },
        {
          "id": "VEQ",
          "value": "Q",
          "owasp_scp": [
            10,
            15,
            16,
            19,
            20
          ],
          "owasp_asvs": [
            5.15,
            5.22,
            5.23,
            5.24,
            5.25
          ],
          "owasp_appsensor": [
            "IE1",
            "RP3"
          ],
          "capec": [
            28,
            31,
            152,
            160,
            468
          ],
          "safecode": [
            2,
            17
          ]
        },
        {
          "id": "VEK",
          "value": "K",
          "owasp_scp": [
            15,
            19,
            20,
            21,
            22,
            167,
            180,
            204,
            211,
            212
          ],
          "owasp_asvs": [
            "5.10",
            5.11,
            5.12,
            5.13,
            5.14,
            5.16,
            5.21
          ],
          "owasp_appsensor": [
            "CIE1",
            "CIE2"
          ],
          "capec": [
            23,
            28,
            76,
            152,
            160,
            261
          ],
          "safecode": [
            2,
            19,
            20
          ]
        }
      ]
    },
    {
      "id": "AT",
      "name": "AUTHENTICATION",
      "cards": [
        {
          "id": "AT2",
          "value": "2",
          "owasp_scp": [
            47,
            52
          ],
          "owasp_asvs": [
            2.12,
            8.4,
            "8.10"
          ],
          "owasp_appsensor": [
            "UT1"
          ],
          "capec": [],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT3",
          "value": "3",
          "owasp_scp": [
            36,
            37,
            40,
            43,
            48,
            51,
            119,
            139,
            140,
            146
          ],
          "owasp_asvs": [
            2.2,
            2.17,
            2.24,
            8.7,
            9.1,
            9.4,
            9.5,
            9.9,
            9.11
          ],
          "owasp_appsensor": [],
          "capec": [
            37,
            546
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT4",
          "value": "4",
          "owasp_scp": [
            33,
            53
          ],
          "owasp_asvs": [
            2.18,
            2.28
          ],
          "owasp_appsensor": [
            "AE1"
          ],
          "capec": [
            383
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT5",
          "value": "5",
          "owasp_scp": [
            54,
            175,
            178
          ],
          "owasp_asvs": [
            2.19
          ],
          "owasp_appsensor": [
            "AE12",
            "HT3"
          ],
          "capec": [
            70
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT6",
          "value": "6",
          "owasp_scp": [
            37,
            45,
            46,
            178
          ],
          "owasp_asvs": [
            2.22
          ],
          "owasp_appsensor": [],
          "capec": [
            50
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT7",
          "value": "7",
          "owasp_scp": [
            33,
            38,
            39,
            41,
            50,
            53
          ],
          "owasp_asvs": [
            2.7,
            "2.20",
            2.23,
            2.25,
            2.27
          ],
          "owasp_appsensor": [
            "AE2",
            "AE3"
          ],
          "capec": [
            2,
            16
          ],
          "safecode": [
            27
          ]
        },
        {
          "id": "AT8",
          "value": "8",
          "owasp_scp": [
            28
          ],
          "owasp_asvs": [
            2.6
          ],
          "owasp_appsensor": [],
          "capec": [
            115
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "AT9",
          "value": "9",
          "owasp_scp": [
            55,
            56
          ],
          "owasp_asvs": [
            2.1,
            2.9,
            2.26,
            2.31,
            4.15
          ],
          "owasp_appsensor": [],
          "capec": [
            21
          ],
          "safecode": [
            14,
            28
          ]
        },
        {
          "id": "ATX",
          "value": "10",
          "owasp_scp": [
            25,
            26,
            27
          ],
          "owasp_asvs": [
            1.7,
            "2.30"
          ],
          "owasp_appsensor": [],
          "capec": [
            90,
            115
          ],
          "safecode": [
            14,
            28
          ]
        },
        {
          "id": "ATJ",
          "value": "J",
          "owasp_scp": [
            23,
            32,
            34
          ],
          "owasp_asvs": [
            2.1
          ],
          "owasp_appsensor": [],
          "capec": [
            115
          ],
          "safecode": [
            14,
            28
          ]
        },
        {
          "id": "ATQ",
          "value": "Q",
          "owasp_scp": [
            23,
            29,
            42,
            49
          ],
          "owasp_asvs": [
            2.1,
            2.8
          ],
          "owasp_appsensor": [],
          "capec": [
            36,
            50,
            115,
            121,
            179
          ],
          "safecode": [
            14,
            28
          ]
        },
        {
          "id": "ATK",
          "value": "K",
          "owasp_scp": [
            24
          ],
          "owasp_asvs": [
            2.4,
            13.2
          ],
          "owasp_appsensor": [],
          "capec": [
            115,
            207,
            554
          ],
          "safecode": [
            14,
            28
          ]
        }
      ]
    },
    {
      "id": "SM",
      "name": "SESSION MANAGEMENT",
      "cards": [
        {
          "id": "SM2",
          "value": "2",
          "owasp_scp": [
            58,
            59
          ],
          "owasp_asvs": [
            "3.10"
          ],
          "owasp_appsensor": [
            "SE2"
          ],
          "capec": [
            31,
            60,
            61
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM3",
          "value": "3",
          "owasp_scp": [
            68
          ],
          "owasp_asvs": [
            3.16,
            3.17,
            3.18
          ],
          "owasp_appsensor": [],
          "capec": [],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM4",
          "value": "4",
          "owasp_scp": [
            59,
            61
          ],
          "owasp_asvs": [
            3.12
          ],
          "owasp_appsensor": [
            "SE2"
          ],
          "capec": [
            31,
            61
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM5",
          "value": "5",
          "owasp_scp": [
            60,
            62,
            66,
            67,
            71,
            72
          ],
          "owasp_asvs": [
            3.2,
            3.7,
            3.11
          ],
          "owasp_appsensor": [
            "SE4-6"
          ],
          "capec": [
            31
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM6",
          "value": "6",
          "owasp_scp": [
            64,
            65
          ],
          "owasp_asvs": [
            3.3,
            3.4,
            3.16,
            3.17,
            3.18
          ],
          "owasp_appsensor": [
            "SE5",
            "SE6"
          ],
          "capec": [
            21
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM7",
          "value": "7",
          "owasp_scp": [
            62,
            63
          ],
          "owasp_asvs": [
            3.2,
            3.5
          ],
          "owasp_appsensor": [],
          "capec": [
            21
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM8",
          "value": "8",
          "owasp_scp": [
            96
          ],
          "owasp_asvs": [],
          "owasp_appsensor": [],
          "capec": [
            21
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SM9",
          "value": "9",
          "owasp_scp": [
            69,
            75,
            76,
            119,
            138
          ],
          "owasp_asvs": [
            3.6,
            8.7,
            10.3
          ],
          "owasp_appsensor": [
            "SE4-6"
          ],
          "capec": [
            31,
            60
          ],
          "safecode": [
            28
          ]
        },
        {
          "id": "SMX",
          "value": "10",
          "owasp_scp": [
            73,
            74
          ],
          "owasp_asvs": [
            4.13
          ],
          "owasp_appsensor": [
            "IE4"
          ],
          "capec": [
            62,
            111
          ],
          "safecode": [
            18
          ]
        },
        {
          "id": "SMJ",
          "value": "J",
          "owasp_scp": [],
          "owasp_asvs": [
            15.1,
            15.2
          ],
          "owasp_appsensor": [
            "IE5"
          ],
          "capec": [
            60
          ],
          "safecode": [
            12,
            14
          ]
        },
        {
          "id": "SMQ",
          "value": "Q",
          "owasp_scp": [
            58
          ],
          "owasp_asvs": [
            3.1
          ],
          "owasp_appsensor": [],
          "capec": [
            21
          ],
          "safecode": [
            14,
            28
          ]
        },
        {
          "id": "SMK",
          "value": "K",
          "owasp_scp": [
            58,
            60
          ],
          "owasp_asvs": [
            1.7
          ],
          "owasp_appsensor": [],
          "capec": [
            21
          ],
          "safecode": [
            14,
            28
          ]
        }
      ]
    },
    {
      "id": "AZ",
      "name": "AUTHORIZATION",
      "cards": [
        {
          "id": "AZ2",
          "value": "2",
          "owasp_scp": [
            44
          ],
          "owasp_asvs": [
            4.1,
            4.16,
            16.1
          ],
          "owasp_appsensor": [],
          "capec": [
            153
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZ3",
          "value": "3",
          "owasp_scp": [
            51,
            100,
            135,
            139,
            140,
            141,
            150
          ],
          "owasp_asvs": [
            4.1,
            8.2,
            "9.1-9.6",
            9.11,
            "16.6-16.7"
          ],
          "owasp_appsensor": [],
          "capec": [
            69,
            213
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZ4",
          "value": "4",
          "owasp_scp": [
            79,
            80
          ],
          "owasp_asvs": [
            4.8
          ],
          "owasp_appsensor": [],
          "capec": [
            122
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZ5",
          "value": "5",
          "owasp_scp": [
            70,
            81,
            "83-4",
            "87-9",
            99,
            117,
            "131-2",
            142,
            154,
            170,
            179
          ],
          "owasp_asvs": [
            4.1,
            4.4,
            4.9,
            19.3
          ],
          "owasp_appsensor": [
            "ATE1",
            "ATE2",
            "ATE3",
            "ATE4",
            "HT2"
          ],
          "capec": [
            75,
            87,
            95,
            126,
            149,
            155,
            203,
            213,
            264,
            265
          ],
          "safecode": [
            8,
            10,
            11,
            13
          ]
        },
        {
          "id": "AZ6",
          "value": "6",
          "owasp_scp": [
            81,
            88,
            131
          ],
          "owasp_asvs": [
            4.1,
            4.4
          ],
          "owasp_appsensor": [
            "ATE1-4"
          ],
          "capec": [
            122
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZ7",
          "value": "7",
          "owasp_scp": [
            81,
            85,
            86,
            131
          ],
          "owasp_asvs": [
            4.1,
            4.4
          ],
          "owasp_appsensor": [
            "ATE1-4"
          ],
          "capec": [
            122
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZ8",
          "value": "8",
          "owasp_scp": [
            10,
            32,
            93,
            94,
            189
          ],
          "owasp_asvs": [
            "4.10",
            4.15,
            4.16,
            8.13,
            15.1
          ],
          "owasp_appsensor": [
            "ATE3"
          ],
          "capec": [
            25,
            39,
            74,
            162,
            166,
            207
          ],
          "safecode": [
            8,
            10,
            11,
            12
          ]
        },
        {
          "id": "AZ9",
          "value": "9",
          "owasp_scp": [
            94
          ],
          "owasp_asvs": [
            4.14,
            15.2
          ],
          "owasp_appsensor": [
            "AE3",
            "FIO1-2",
            "UT2-4",
            "STE1-3"
          ],
          "capec": [
            26,
            29,
            119,
            261
          ],
          "safecode": [
            1,
            35
          ]
        },
        {
          "id": "AZX",
          "value": "10",
          "owasp_scp": [
            78,
            91
          ],
          "owasp_asvs": [
            1.7,
            4.11
          ],
          "owasp_appsensor": [
            "ATE1-4"
          ],
          "capec": [
            36,
            95,
            121,
            179
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZJ",
          "value": "J",
          "owasp_scp": [
            89,
            90
          ],
          "owasp_asvs": [
            "4.10",
            13.2
          ],
          "owasp_appsensor": [],
          "capec": [
            75,
            133,
            203
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZQ",
          "value": "Q",
          "owasp_scp": [
            209
          ],
          "owasp_asvs": [
            5.12
          ],
          "owasp_appsensor": [],
          "capec": [
            17,
            30,
            69,
            234
          ],
          "safecode": [
            8,
            10,
            11
          ]
        },
        {
          "id": "AZK",
          "value": "K",
          "owasp_scp": [
            77,
            89,
            91
          ],
          "owasp_asvs": [
            4.9,
            "4.10",
            13.2
          ],
          "owasp_appsensor": [],
          "capec": [
            207,
            554
          ],
          "safecode": [
            8,
            10,
            11
          ]
        }
      ]
    },
    {
      "id": "CR",
      "name": "CRYPTOGRAPHY",
      "cards": [
        {
          "id": "CR2",
          "value": "2",
          "owasp_scp": [
            105,
            133,
            135
          ],
          "owasp_asvs": [],
          "owasp_appsensor": [],
          "capec": [],
          "safecode": [
            21,
            29
          ]
        },
        {
          "id": "CR3",
          "value": "3",
          "owasp_scp": [
            92,
            205,
            212
          ],
          "owasp_asvs": [
            8.11,
            11.7,
            13.2,
            19.5,
            19.6,
            19.7,
            19.8
          ],
          "owasp_appsensor": [
            "SE1",
            "IE4"
          ],
          "capec": [
            31,
            39,
            68,
            75,
            133,
            145,
            162,
            203,
            438,
            439,
            442
          ],
          "safecode": [
            12,
            14
          ]
        },
        {
          "id": "CR4",
          "value": "4",
          "owasp_scp": [
            37,
            88,
            143,
            214
          ],
          "owasp_asvs": [
            7.12,
            9.2
          ],
          "owasp_appsensor": [],
          "capec": [
            185,
            186,
            187
          ],
          "safecode": [
            14,
            29,
            30
          ]
        },
        {
          "id": "CR5",
          "value": "5",
          "owasp_scp": [
            103,
            145
          ],
          "owasp_asvs": [
            7.2,
            10.3
          ],
          "owasp_appsensor": [],
          "capec": [],
          "safecode": [
            21,
            29
          ]
        },
        {
          "id": "CR6",
          "value": "6",
          "owasp_scp": [
            36,
            37,
            143,
            146,
            147
          ],
          "owasp_asvs": [
            2.16,
            9.2,
            9.11,
            10.3,
            19.2
          ],
          "owasp_appsensor": [],
          "capec": [
            31,
            57,
            102,
            157,
            158,
            384,
            466,
            546
          ],
          "safecode": [
            29
          ]
        },
        {
          "id": "CR7",
          "value": "7",
          "owasp_scp": [
            75,
            144,
            145,
            148
          ],
          "owasp_asvs": [
            10.1,
            10.5,
            "10.10",
            10.11,
            10.12,
            10.13,
            10.14
          ],
          "owasp_appsensor": [
            "IE4"
          ],
          "capec": [
            31,
            216
          ],
          "safecode": [
            14,
            29,
            30
          ]
        },
        {
          "id": "CR8",
          "value": "8",
          "owasp_scp": [
            30,
            31,
            70,
            133,
            135
          ],
          "owasp_asvs": [
            2.13,
            7.7,
            7.8,
            9.2
          ],
          "owasp_appsensor": [],
          "capec": [
            31,
            37,
            55
          ],
          "safecode": [
            21,
            29,
            31
          ]
        },
        {
          "id": "CR9",
          "value": "9",
          "owasp_scp": [
            60,
            104,
            105
          ],
          "owasp_asvs": [
            7.6,
            7.7,
            7.8,
            7.15
          ],
          "owasp_appsensor": [],
          "capec": [
            97
          ],
          "safecode": [
            14,
            21,
            29,
            32,
            33
          ]
        },
        {
          "id": "CRX",
          "value": "10",
          "owasp_scp": [
            104,
            105
          ],
          "owasp_asvs": [],
          "owasp_appsensor": [],
          "capec": [
            97,
            463
          ],
          "safecode": [
            14,
            21,
            29,
            31,
            32,
            33
          ]
        },
        {
          "id": "CRJ",
          "value": "J",
          "owasp_scp": [
            35,
            90,
            171,
            172
          ],
          "owasp_asvs": [
            2.29
          ],
          "owasp_appsensor": [],
          "capec": [
            116
          ],
          "safecode": [
            21,
            29
          ]
        },
        {
          "id": "CRQ",
          "value": "Q",
          "owasp_scp": [
            35,
            102
          ],
          "owasp_asvs": [
            7.8,
            7.9,
            7.11,
            7.13,
            7.14
          ],
          "owasp_appsensor": [],
          "capec": [
            116,
            117
          ],
          "safecode": [
            21,
            29
          ]
        },
        {
          "id": "CRK",
          "value": "K",
          "owasp_scp": [
            31,
            101
          ],
          "owasp_asvs": [
            7.11
          ],
          "owasp_appsensor": [],
          "capec": [
            207,
            554
          ],
          "safecode": [
            14,
            21,
            29
          ]
        }
      ]
    },
    {
      "id": "C",
      "name": "CORNUCOPIA",
      "cards": [
        {
          "id": "C2",
          "value": "2",
          "owasp_scp": [
            194,
            195,
            196,
            197,
            198,
            199,
            200,
            201,
            202,
            205,
            206,
            207,
            208,
            209
          ],
          "owasp_asvs": [
            5.1
          ],
          "owasp_appsensor": [],
          "capec": [
            25,
            26,
            29,
            96,
            123,
            124,
            128,
            129,
            264,
            265
          ],
          "safecode": [
            3,
            5,
            6,
            7,
            9,
            22,
            25,
            26,
            34
          ]
        },
        {
          "id": "C3",
          "value": "3",
          "owasp_scp": [
            134
          ],
          "owasp_asvs": [
            19.5
          ],
          "owasp_appsensor": [],
          "capec": [
            189,
            207
          ],
          "safecode": []
        },
        {
          "id": "C4",
          "value": "4",
          "owasp_scp": [
            23,
            32,
            34,
            42,
            51,
            181
          ],
          "owasp_asvs": [
            "8.10"
          ],
          "owasp_appsensor": [],
          "capec": [],
          "safecode": []
        },
        {
          "id": "C5",
          "value": "5",
          "owasp_scp": [],
          "owasp_asvs": [],
          "owasp_appsensor": [],
          "capec": [
            89,
            103,
            181,
            459
          ],
          "safecode": []
        },
        {
          "id": "C6",
          "value": "6",
          "owasp_scp": [
            109,
            110,
            111,
            112,
            155
          ],
          "owasp_asvs": [
            8.2,
            8.4
          ],
          "owasp_appsensor": [],
          "capec": [
            54,
            98,
            164
          ],
          "safecode": [
            4,
            11,
            23
          ]
        },
        {
          "id": "C7",
          "value": "7",
          "owasp_scp": [
            113,
            114,
            115,
            117,
            118,
            121,
            122,
            123,
            124,
            125,
            126,
            127,
            128,
            129,
            130
          ],
          "owasp_asvs": [
            2.12,
            8.3,
            8.4,
            8.5,
            8.6,
            8.7,
            8.8,
            8.9,
            "8.10",
            8.11,
            8.12,
            "9.10",
            10.4
          ],
          "owasp_appsensor": [],
          "capec": [
            93
          ],
          "safecode": [
            4
          ]
        },
        {
          "id": "C8",
          "value": "8",
          "owasp_scp": [
            151,
            152,
            156,
            160,
            161,
            173,
            174,
            175,
            176,
            177
          ],
          "owasp_asvs": [
            19.1,
            19.4,
            19.6,
            19.7,
            19.8
          ],
          "owasp_appsensor": [
            "RE1",
            "RE2"
          ],
          "capec": [
            37,
            220,
            310,
            436,
            536
          ],
          "safecode": []
        },
        {
          "id": "C9",
          "value": "9",
          "owasp_scp": [
            23,
            29,
            56,
            81,
            82,
            84,
            85,
            86,
            87,
            88,
            89,
            90
          ],
          "owasp_asvs": [
            2.1,
            2.32
          ],
          "owasp_appsensor": [],
          "capec": [
            122,
            233
          ],
          "safecode": []
        },
        {
          "id": "CX",
          "value": "10",
          "owasp_scp": [
            57,
            151,
            152,
            204,
            205,
            213,
            214
          ],
          "owasp_asvs": [
            1.11
          ],
          "owasp_appsensor": [],
          "capec": [
            68,
            438,
            439,
            442,
            524,
            538
          ],
          "safecode": [
            15
          ]
        },
        {
          "id": "CJ",
          "value": "J",
          "owasp_scp": [
            90,
            137,
            148,
            151,
            152,
            153,
            154,
            175,
            176,
            177,
            178,
            179,
            186,
            192
          ],
          "owasp_asvs": [
            19.5,
            19.9
          ],
          "owasp_appsensor": [],
          "capec": [],
          "safecode": [
            4
          ]
        },
        {
          "id": "CQ",
          "value": "Q",
          "owasp_scp": [],
          "owasp_asvs": [
            4.14,
            9.8,
            15.1,
            15.2
          ],
          "owasp_appsensor": [
            "(All)"
          ],
          "capec": [],
          "safecode": [
            1,
            27
          ]
        },
        {
          "id": "CK",
          "value": "K",
          "owasp_scp": [
            41,
            55
          ],
          "owasp_asvs": [],
          "owasp_appsensor": [
            "UT1-4",
            "STE3"
          ],
          "capec": [
            2,
            25,
            119,
            125
          ],
          "safecode": [
            1
          ]
        }
      ]
    }
  ]
}

  export default mappings