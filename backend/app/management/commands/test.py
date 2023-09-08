import unittest

import coverage
from django.core.management.base import BaseCommand

from app.settings import BASE_DIR

COV = coverage.coverage(branch=True, include=["utils/*", "user/*", "post/*"])
COV.start()


class Command(BaseCommand):
    help = "Run the unit tests"

    def add_arguments(self, parser):
        # FIXME: Regrex filter does not work
        parser.add_argument(
            "--filter", type=str, default=r"(test_api|test_basic|test_e2e)"
        )

    def handle(self, *args, **options):
        print(f"Filter: {options['filter']}")

        loader = unittest.TestLoader()
        loader.testNamePatterns = (
            [options["filter"] + "*"] if options["filter"] else None
        )
        print("options['filter'] = ", options["filter"] + "*")
        tests = loader.discover(str(BASE_DIR) + "/tests")
        unittest.TextTestRunner(verbosity=2).run(tests)
        COV.stop()
        COV.save()
        print("\n\nCoverage Report:\n")
        COV.report()
