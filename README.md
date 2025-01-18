![](https://github.com/hasii2011/code-ally-basic/blob/master/developer/agpl-license-web-badge-version-2-256x48.png "AGPL")

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity)
[![CircleCI](https://dl.circleci.com/status-badge/img/gh/hasii2011/pyutplugins/tree/master.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/hasii2011/pyutplugins/tree/master)
[![PyPI version](https://badge.fury.io/py/pyutplugins.svg)](https://badge.fury.io/py/pyutplugins)

[![CircleCI](https://dl.circleci.com/insights-snapshot/gh/hasii2011/pyutplugins/master/main/badge.svg?window=30d)](https://app.circleci.com/insights/github/hasii2011/pyutplugins/workflows/main/overview?branch=master&reporting-window=last-30-days&insights-snapshot=true)


# Introduction
This module houses the plugins that enhance the capabilities of [Pyut](https://github.com/hasii2011/pyut).  This separate module allows external developers to write plugins external to Pyut.  This module includes a "Scaffold Application" that allows developers to test drive their plugins prior to integrating them into Pyut.

# Plugin Development

See the following [document](https://github.com/hasii2011/pyutplugins/wiki/Pyut-Plugin-Development) for additional details on how to develop Pyut plugins

## Developer Notes

This project uses [buildlackey](https://github.com/hasii2011/buildlackey) for day to day development builds

Also notice that this project does not include a `requirements.txt` file.  All dependencies are listed in the `pyproject.toml` file.

#### Install the main project dependencies

```bash
pip install .
```

#### Install the test dependencies

```bash
pip install .[test]
```

#### Install the deploy dependencies

```bash
pip install .[deploy]
```

Normally, not needed because the project uses a GitHub workflow that automatically deploys releases

___

Written by <a href="mailto:email@humberto.a.sanchez.ii@gmail.com?subject=Hello Humberto">Humberto A. Sanchez II</a>  (C) 2025

___

I am concerned about GitHub's Copilot project

![](https://github.com/hasii2011/code-ally-basic/blob/master/developer/SillyGitHub.png)

I urge you to read about the
[Give up GitHub](https://GiveUpGitHub.org) campaign from
[the Software Freedom Conservancy](https://sfconservancy.org).

While I do not advocate for all the issues listed there I do not like that a company like Microsoft may profit from open source projects.

I continue to use GitHub because it offers the services I need for free.  But, I continue to monitor their terms of service.

Any use of this project's code by GitHub Copilot, past or present, is done without my permission.  I do not consent to GitHub's use of this project's code in Copilot.
