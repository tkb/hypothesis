# coding=utf-8

# Copyright (C) 2013-2015 David R. MacIver (david@drmaciver.com)

# This file is part of Hypothesis (https://github.com/DRMacIver/hypothesis)

# This Source Code Form is subject to the terms of the Mozilla Public License,
# v. 2.0. If a copy of the MPL was not distributed with this file, You can
# obtain one at http://mozilla.org/MPL/2.0/.

# END HEADER

from __future__ import division, print_function, absolute_import, \
    unicode_literals

import pytest
from hypothesis import Settings

TEST_DESCRIPTION = 'This is a setting just for these tests'

Settings.define_setting(
    'a_setting_just_for_these_tests',
    default=3,
    description=TEST_DESCRIPTION,
)


def test_has_docstrings():
    assert TEST_DESCRIPTION in Settings.a_setting_just_for_these_tests.__doc__


def setup_function(fn):
    try:
        delattr(Settings.default, 'a_setting_just_for_these_tests')
    except AttributeError:
        pass


def test_cannot_set_non_settings():
    s = Settings()
    with pytest.raises(AttributeError):
        s.databas_file = 'some_file'


def test_settings_uses_defaults():
    s = Settings()
    assert s.a_setting_just_for_these_tests == 3


def test_picks_up_changes_to_defaults():
    Settings.default.a_setting_just_for_these_tests = 18
    assert Settings.default.a_setting_just_for_these_tests == 18
    s = Settings()
    assert s.a_setting_just_for_these_tests == 18


def test_does_not_pick_up_changes_after_instantiation():
    s = Settings()
    Settings.default.a_setting_just_for_these_tests = 18
    assert s.a_setting_just_for_these_tests == 3


def test_raises_attribute_error():
    with pytest.raises(AttributeError):
        Settings().kittens


def test_respects_none_database():
    assert Settings(database=None).database is None


def test_settings_can_be_used_as_context_manager_to_change_defaults():
    with Settings(a_setting_just_for_these_tests=12):
        assert Settings.default.a_setting_just_for_these_tests == 12
    assert Settings.default.a_setting_just_for_these_tests == 3


def test_can_repeatedly_push_the_same_thing():
    s = Settings(a_setting_just_for_these_tests=12)
    t = Settings(a_setting_just_for_these_tests=17)
    assert Settings().a_setting_just_for_these_tests == 3
    with s:
        assert Settings().a_setting_just_for_these_tests == 12
        with t:
            assert Settings().a_setting_just_for_these_tests == 17
            with s:
                assert Settings().a_setting_just_for_these_tests == 12
                with t:
                    assert Settings().a_setting_just_for_these_tests == 17
                assert Settings().a_setting_just_for_these_tests == 12
            assert Settings().a_setting_just_for_these_tests == 17
        assert Settings().a_setting_just_for_these_tests == 12
    assert Settings().a_setting_just_for_these_tests == 3
