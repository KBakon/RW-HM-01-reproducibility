# Python environment

Standard-library Python only; no pip package, external solver, platform account or network access is required. This assembly used CPython 3.13.15. Use Python 3.10 or later (tested here on 3.13.15); other versions were not executed during assembly. No third-party module named common is required: the original local wp1_generalization/common.py is included.

The sibling layout is part of the runtime contract. Run documented commands from the reproducibility root. The WP2 and WP3 entry scripts prepend sibling wp1_generalization to sys.path. Campaign modules with top-level loops must not be imported as smoke tests; syntax compilation is safe and library imports are checked separately. Full campaigns were not run during assembly. The original exact searches have instance timeouts; these and historical UNSOLVED_RESOURCE_BOUND statuses are not altered.
