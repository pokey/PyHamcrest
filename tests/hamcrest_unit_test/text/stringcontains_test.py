from __future__ import with_statement
import six
from hamcrest.library.text.stringcontains import contains_string
from hamcrest_unit_test.matcher_test import *
import unittest
import pytest

__author__ = "Jon Reid"
__copyright__ = "Copyright 2011 hamcrest.org"
__license__ = "BSD, see License.txt"


if six.PY2:
    matcher_args = ("EXCERPT", six.u("EXCERPT"))
else:
    matcher_args = ("EXCERPT",)

    
@pytest.fixture(scope="module",
                params=matcher_args)
def matcher(request):
    return contains_string(request.param)

TEST_MATCHING_STRINGS = (
    ("EXCERPTEND",),
    ("STARTEXCERPTEND",),
    ("STARTEXCERPT",),
    ("EXCERPTEXCERPT",),
    ("EXCERPT",),
)
if six.PY2:
    TEST_MATCHING_STRINGS += (
        (six.u("EXCERPTEND"),),
        (six.u("STARTEXCERPTEND"),),
        (six.u("STARTEXCERPT"),),
        (six.u("EXCERPTEXCERPT"),),
        (six.u("EXCERPT"),),
    )

TEST_MISMATCHING_STRINGS = (
    ("whatever",),
    ("EXCERP",),
    (object(),),
)


@pytest.mark.parametrize(['text'], TEST_MATCHING_STRINGS)
def test_evaluates_true_if_argument_contains_substring(text, matcher):
    assert_matches(matcher, text, "assert that %s matches %s" % (text, matcher))


@pytest.mark.parametrize(['text'], TEST_MISMATCHING_STRINGS)
def test_evaluates_false_with_mismatch(text, matcher):
    assert_does_not_match(matcher, text, "%s was not in string %s" % (matcher, text))


def testMatcherCreationRequiresString():
    with pytest.raises(TypeError):
        contains_string(3)


def test_description(matcher):
    assert_description("a string containing 'EXCERPT'", matcher)


def test_successful_match_does_not_have_mismatch_description(matcher):
    assert_no_mismatch_description(matcher, "EXCERPT")


@pytest.mark.parametrize(['text'], TEST_MISMATCHING_STRINGS)
def test_mismatch_description(matcher, text):
    if isinstance(text, six.string_types):
        check_str = "'%s'" % text
    else:
        check_str = "%s" % text
    assert_mismatch_description("was %s" % check_str, matcher, text)


if __name__ == '__main__':
    unittest.main()
