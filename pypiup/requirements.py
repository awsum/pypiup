# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import click
import pkg_resources

from pypiup.requirement import Requirement


class Requirements(object):

    def __init__(self, requirements_file):
        self.file = self.read_file(requirements_file)
        self.requirements = []

    def read_file(self, requirements_filename):
        click.secho("\nAttempting to read %s ...\n" % requirements_filename, fg='magenta')

        try:
            requirements_data = open(requirements_filename).read()
            requirements_lines = pkg_resources.yield_lines(requirements_data)
            with click.progressbar(
                    iterable=requirements_lines,
                    label='Getting requirements details',
                    bar_template='%(label)s %(bar)s | %(info)s',
                    fill_char=click.style(u'█', fg='cyan'),
                    empty_char=' ') as bar:
                self.requirements = [Requirement(line) for line in bar]
                self.show_details()
                self.show_stats()
        except IOError:
            return click.secho("Could not find %s. No such file or directory.\n" % (requirements_filename), fg='red')

    def show_details(self):
        click.echo()
        for requirement in self.requirements:
            requirement.output_details()

    def show_stats(self):
        stat_total = len(self.requirements)
        stat_uptodate = 0
        stat_needs_update = 0
        stat_invalid_semver = 0
        stat_invalid = 0

        for requirement in self.requirements:
            if requirement.valid:
                if requirement.status == "UPTODATE":
                    stat_uptodate += 1
                elif requirement.status == "NEEDS_UPDATE":
                    stat_needs_update += 1
                elif requirement.status == "INVALID_SEMVER":
                    stat_invalid_semver += 1
            else:
                stat_invalid += 1

        click.echo(click.style("\nStatistics", bold=True, underline=True, fg='yellow'))
        click.echo("  Total Requirements: %s" % stat_total)
        click.echo("  Up to date: %s" % stat_uptodate)
        click.echo("  Update available: %s" % stat_needs_update)
        click.echo("  Invalid Semver: %s" % stat_invalid_semver)
        click.echo("  Non PyPI Requirements: %s" % stat_invalid)
