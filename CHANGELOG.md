# Changelog

## [1.1.4](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.1.3...v1.1.4) (2023-03-26)


### Bug Fixes

* try just doing it on the release tag ([03937b4](https://github.com/pcn/windmill-eks-iam-helper/commit/03937b4fc4e2efe554dfdfad90bb17d3f6d4ed78))

## [1.1.3](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.1.2...v1.1.3) (2023-03-26)


### Bug Fixes

* muddle through more tag stuff ([daccc74](https://github.com/pcn/windmill-eks-iam-helper/commit/daccc74b0d93fa530b9b7a5a6a8d9e946da5b32b))

## [1.1.2](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.1.1...v1.1.2) (2023-03-26)


### Bug Fixes

* try to debug this permissins error ([a0effab](https://github.com/pcn/windmill-eks-iam-helper/commit/a0effab6cc5c74dfbfa6f5a00c2353b25d894962))

## [1.1.1](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.1.0...v1.1.1) (2023-03-26)


### Bug Fixes

* update changelog and fix tagging the image ([728d155](https://github.com/pcn/windmill-eks-iam-helper/commit/728d1556d56e624ed15df42810f8e323417a0a86))

## [1.1.0](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.12...v1.1.0) (2023-03-26)


### Features

* work on using resources instead of one big variable ([#49](https://github.com/pcn/windmill-eks-iam-helper/issues/49)) ([eebb0d4](https://github.com/pcn/windmill-eks-iam-helper/commit/eebb0d440a7b442f5e6296817d4daf502e35f916))

## [1.0.12](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.11...v1.0.12) (2023-03-24)


### Bug Fixes

* breaks when missing this now ([411003e](https://github.com/pcn/windmill-eks-iam-helper/commit/411003edb07965cdb94f6a9d47ca338edf9e83b8))
* restore default=str behavior ([aa70dec](https://github.com/pcn/windmill-eks-iam-helper/commit/aa70dec5802b4c39b0662b5f8d4e5f711a751334))
* slightly different calls based on create or update ([e43c53f](https://github.com/pcn/windmill-eks-iam-helper/commit/e43c53f41822a39fc8be16f0eef0d5107339bec5))

## [1.0.11](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.10...v1.0.11) (2023-01-14)


### Bug Fixes

* set a default BASE_INTERNAL_URL if none is set ([edea9f6](https://github.com/pcn/windmill-eks-iam-helper/commit/edea9f679fc01ccb38111def93fe383ab399fcfa))

## [1.0.10](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.9...v1.0.10) (2023-01-13)


### Bug Fixes

* Allow increating timeouts to troubleshoot a problematic pod ([8914b71](https://github.com/pcn/windmill-eks-iam-helper/commit/8914b71a932d11ff070155fbfaf714174d34a62f))

## [1.0.9](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.8...v1.0.9) (2023-01-13)


### Bug Fixes

* log the sleeping ([02a21fd](https://github.com/pcn/windmill-eks-iam-helper/commit/02a21fdeeb01a82aff841980367a1708bbcfe0e9))

## [1.0.8](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.7...v1.0.8) (2023-01-13)


### Bug Fixes

* make the iam prefix env variable slightly longer ([e0d5233](https://github.com/pcn/windmill-eks-iam-helper/commit/e0d5233f1efff917ba86dea334ecca89d921c9e5))
* type returned by os.getenv is str ([4fca826](https://github.com/pcn/windmill-eks-iam-helper/commit/4fca826f9ddeaa658b581437d8e483a07874c29d))

## [1.0.7](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.6...v1.0.7) (2023-01-13)


### Bug Fixes

* and log time on each loop ([dbfc777](https://github.com/pcn/windmill-eks-iam-helper/commit/dbfc77710d9f1861e6503c0053258412ceb46b8b))
* make the sleep interval a setting, default to 5 minutes ([efbfda5](https://github.com/pcn/windmill-eks-iam-helper/commit/efbfda55a8c68321a211ae555a57bd376b22acfc))
* syntax error ([4db0dba](https://github.com/pcn/windmill-eks-iam-helper/commit/4db0dba5c68c6c06299deff58c9cc457f30db8ee))

## [1.0.7](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.6...v1.0.7) (2023-01-13)


### Bug Fixes

* and log time on each loop ([dbfc777](https://github.com/pcn/windmill-eks-iam-helper/commit/dbfc77710d9f1861e6503c0053258412ceb46b8b))
* make the sleep interval a setting, default to 5 minutes ([efbfda5](https://github.com/pcn/windmill-eks-iam-helper/commit/efbfda55a8c68321a211ae555a57bd376b22acfc))

## [1.0.6](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.5...v1.0.6) (2023-01-13)


### Bug Fixes

* don't die on lack of connection ([964db68](https://github.com/pcn/windmill-eks-iam-helper/commit/964db688c5a53b1dc6824ba3e0fffa56978987bd))

## [1.0.5](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.4...v1.0.5) (2023-01-11)


### Bug Fixes

* add modules the normal way ([41d9df5](https://github.com/pcn/windmill-eks-iam-helper/commit/41d9df52a3f2b645934621c937b88a528a815266))
* works, adds credentials called "iam" to the "aws" folder ([fda5fef](https://github.com/pcn/windmill-eks-iam-helper/commit/fda5fef133a4578d79fbf7754c0f72090a7c8553))

## [1.0.4](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.3...v1.0.4) (2023-01-09)


### Bug Fixes

* try to update this for goodness sake ([c184a69](https://github.com/pcn/windmill-eks-iam-helper/commit/c184a6992b093c4a780f0561ccbf1790e29a05fe))

## [1.0.3](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.2...v1.0.3) (2023-01-09)


### Bug Fixes

* Use a PAT to avoid recursive invocation protection ([163bee2](https://github.com/pcn/windmill-eks-iam-helper/commit/163bee2d5522a46b55df5cf687241e70ea462dc7))

## [1.0.2](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.1...v1.0.2) (2023-01-09)


### Bug Fixes

* lots of typos in metadata ([d1d69b1](https://github.com/pcn/windmill-eks-iam-helper/commit/d1d69b1363f4d02c75c7531e147a10a915fd77f3))

## [1.0.1](https://github.com/pcn/windmill-eks-iam-helper/compare/v1.0.0...v1.0.1) (2023-01-09)


### Bug Fixes

* If an execption goes all the way to the top, slow down the restart ([8957921](https://github.com/pcn/windmill-eks-iam-helper/commit/8957921d8b6d78eff0653edc922f6c3fa6fb88d8))
* loop in main ([7a22d30](https://github.com/pcn/windmill-eks-iam-helper/commit/7a22d308ccd960e9d474b15eed4f0eee16a16787))

## 1.0.0 (2023-01-08)


### Features

* add release-please files ([a504868](https://github.com/pcn/windmill-eks-iam-helper/commit/a504868f118a45810954ddc0681cd28eed869fb6))


### Bug Fixes

* really simple ([5858560](https://github.com/pcn/windmill-eks-iam-helper/commit/5858560c75db070d3aa9eb6c9d10b634479689b3))
* set a path ([dd60535](https://github.com/pcn/windmill-eks-iam-helper/commit/dd605357a034df6bf52b4701946eb42ee84d1df4))
* set type to simple ([224b33f](https://github.com/pcn/windmill-eks-iam-helper/commit/224b33f94e877da4a69b9dd8c908bdcb0547c7e5))
* simplify more ([932b154](https://github.com/pcn/windmill-eks-iam-helper/commit/932b15457b9c10a6d906b1e9813ca642e04f0d4a))
* the package name is set incorrectly ([1338b1b](https://github.com/pcn/windmill-eks-iam-helper/commit/1338b1b79c2a3d79e5fc577f573addb047b25e9a))
* Try doing this automatically ([4f3c214](https://github.com/pcn/windmill-eks-iam-helper/commit/4f3c214fc9822601d6be5d1e26fbefbf8c89b509))
* update action ([3a718b2](https://github.com/pcn/windmill-eks-iam-helper/commit/3a718b2a22cbd39d302f876576870940e12307ef))
* use the script as an entrypoint ([8314b44](https://github.com/pcn/windmill-eks-iam-helper/commit/8314b44d7d0cdc7684d516fb0b9859bf971b9197))
