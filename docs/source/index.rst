.. respondpy documentation master file, created by
   sphinx-quickstart on Wed Jul 15 14:57:47 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to respondpy's documentation!
=====================================

**respondpy** is a Python library for wrapping and interacting with the `RESPOND simulation model`_ C++ API. It provides a convenient and Pythonic interface for users to access the functionality of RESPOND, enabling seamless integration with Python applications.

.. _RESPOND simulation model: https://github.com/SyndemicsLab/respond.git

.. note::
    This project is under active development, and the API may change in future releases. Users are encouraged to check the documentation for updates and refer to the source code for the latest features.

Documentation flow
------------------

The docs are organized into four sections with distinct goals:

- Tutorials: guided learning paths for researchers.
- How-To Guides: task-oriented workflows for engineers embedding RESPOND.
- Explanations: conceptual architecture and runtime behavior.
- References: API and symbol-level technical detail.

Start here based on your goal:

- Learn by doing: Tutorials.
- Complete a concrete task: How-To Guides.
- Understand system design: Explanations.
- Look up precise behavior or signatures: References.

.. toctree::
   :maxdepth: 1

   tutorials/base_respond

.. toctree::
   :maxdepth: 1

   how_to/data_loading

.. toctree::
   :maxdepth: 1

   explanations/architecture

.. toctree::
   :maxdepth: 1

   references/wrapper_typing