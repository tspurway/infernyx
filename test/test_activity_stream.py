import unittest
from itertools import combinations

from infernyx.rule_helpers import activity_stream_session_filter, activity_stream_event_filter,\
    application_stats_filter, clean_activity_stream_session, clean_activity_stream_event,\
    activity_stream_performance_filter, clean_activity_stream_performance, ss_activity_stream_session_filter,\
    ss_activity_stream_event_filter, ss_activity_stream_performance_filter, clean_shield_study_fields,\
    activity_stream_masga_filter, ss_activity_stream_masga_filter, clean_activity_stream_masga


FIXTURE = [
    {"session_duration": 447, "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "click", "client_id": "f172d443-2434-49c2-b91c-fc8fd4ef9eaf", "max_scroll_depth": 167, "addon_version": "1.0.5", "total_history_size": 221, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 200, "click_position": 6, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "5", "load_reason": "focus", "page": "timeline", "total_bookmarks": 7, "highlights_size": 9},
    {"session_duration": 2775, "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "search", "client_id": "f172d443-2434-49c2-b91c-fc8fd4ef9eaf", "max_scroll_depth": 365, "addon_version": "1.0.5", "total_history_size": 191, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 196, "click_position": 18, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "2", "load_reason": "restore", "page": "timeline", "total_bookmarks": 17, "highlights_size": 0},
    {"session_duration": 3095, "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "unfocus", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "max_scroll_depth": 429, "addon_version": "1.0.5", "total_history_size": 324, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 198, "click_position": 5, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "8", "load_reason": "restore", "page": "timeline", "total_bookmarks": 0, "highlights_size": 5},
    {"session_duration": 1257, "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "close", "client_id": "9b57e4af-d96c-4ee2-8918-211a6248fcfc", "max_scroll_depth": 692, "addon_version": "1.0.5", "total_history_size": 359, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 212, "click_position": 19, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "9", "load_reason": "focus", "page": "timeline", "total_bookmarks": 5, "highlights_size": 9},
    {"session_duration": 548, "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "close", "client_id": "93a7579d-c986-4e33-809e-e4101bf523f9", "max_scroll_depth": 61, "addon_version": "1.0.5", "total_history_size": 460, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 216, "click_position": 19, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "5", "load_reason": "focus", "page": "timeline", "total_bookmarks": 3, "highlights_size": 6},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "search", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_event", "tab_id": "4", "ua": "python-requests\/2.9.1", "page": "timeline", "url": "www.test.com", "recommender_type": "recommener_1", "highlight_type": "bookmarks", "provider": "yahoo-mail"},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "f172d443-2434-49c2-b91c-fc8fd4ef9eaf", "date": "2016-04-04", "event": "click", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_event", "tab_id": "9", "ua": "python-requests\/2.9.1", "page": "timeline", "url": "www.test.com", "recommender_type": "recommener_2", "highlight_type": "recommendations", "metadata_source": "Embedly"},
    {"locale": "en-US", "ip": "10.192.171.13", "client_id": "7cfd94f1-880d-40bc-b881-23dbde3560db", "date": "2016-04-04", "event": "search", "addon_version": "1.0.5", "ver": "3", "source": "top_sites", "timestamp": 1459810810000, "action": "activity_stream_event", "tab_id": "9", "ua": "python-requests\/2.9.1", "page": "newtab", "url": "www.test.com", "recommender_type": "recommener_3", "highlight_type": "history"},
    {"locale": "en-US", "ip": "10.192.171.13", "client_id": "4fe8f425-7414-4d83-972a-49104ed7deee", "date": "2016-04-04", "event": "delete", "addon_version": "1.0.5", "ver": "3", "source": "recent_bookmarks", "timestamp": 1459810810000, "action": "activity_stream_event", "tab_id": "7", "ua": "python-requests\/2.9.1", "page": "timeline"},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "04828dba-89ac-444a-ad26-53778b4c2440", "date": "2016-04-04", "event": "click", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_event", "tab_id": "5", "ua": "python-requests\/2.9.1", "page": "newtab"},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheHit", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 10, "metadata_source": "Embedly"},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheMiss", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 130},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheMiss", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 14},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheHit", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 110},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheFetch", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 120},
    {"ver": "3", "locale": "zu", "ip": "15.211.153.0", "date": "2016-02-18", "timestamp": 1455837962657, "action": "fetch_served", "ua": "python-requests/2.9.1", "channel": "hello"},
    {"ver": "3", "locale": "es-CL", "ip": "15.211.153.0", "date": "2016-02-18", "timestamp": 1455837962658, "action": "fetch_served", "ua": "python-requests/2.9.1", "channel": "aurora"},
    {"ver": "3", "locale": "ru", "ip": "15.211.153.0", "date": "2016-02-18", "timestamp": 1455837962661, "action": "fetch_served", "ua": "python-requests/2.9.1", "channel": "aurora"},
    {"ver": "2", "locale": "en-US", "ip": "15.211.153.0", "date": "2016-02-18", "timestamp": 1455837962662, "action": "fetch_served", "ua": "python-requests/2.9.1"},
    {"ver": "3", "locale": "es-MX", "ip": "15.211.153.0", "date": "2016-02-18", "timestamp": 1455837962665, "action": "fetch_served", "ua": "python-requests/2.9.1", "channel": "esr"},
    {"event": "SHOW_LOADER", "source": "NEW_TAB", "value": 5000, "action": "activity_stream_masga_event", "tab_id": "-3-2", "client_id": "a7967bc5-38ea-dd48-bfe9-ee06ca94f7e1", "addon_version": "1.1.8", "locale": "en-US", "page": "NEW_TAB", "session_id": "{d8a1812e-9f38-184c-9eed-01b98d4363e5}", "experiment_id": "exp-005-metadata-service"},
    {"event": "SHOW_LOADER", "source": "NEW_TAB", "value": 1482268703822, "action": "activity_stream_masga_event", "tab_id": "-3-2", "client_id": "a7967bc5-38ea-dd48-bfe9-ee06ca94f7e1", "addon_version": "1.1.8", "locale": "en-US", "page": "NEW_TAB", "session_id": "{d8a1812e-9f38-184c-9eed-01b98d4363e5}", "experiment_id": "exp-005-metadata-service"},
    {"event": "SHOW_LOADER", "source": "NEW_TAB", "value": 5000, "action": "activity_stream_masga_event", "tab_id": "-3-2", "client_id": "a7967bc5-38ea-dd48-bfe9-ee06ca94f7e1", "addon_version": "1.1.8", "locale": "en-US", "page": "NEW_TAB", "session_id": "{d8a1812e-9f38-184c-9eed-01b98d4363e5}", "experiment_id": "exp-005-metadata-service"},
    {"event": "HIDE_LOADER", "source": "NEW_TAB", "value": 7000, "action": "activity_stream_masga_event", "tab_id": "-3-2", "client_id": "a7967bc5-38ea-dd48-bfe9-ee06ca94f7e1", "addon_version": "1.1.8", "locale": "en-US", "page": "NEW_TAB", "session_id": "{d8a1812e-9f38-184c-9eed-01b98d4363e5}", "experiment_id": "exp-005-metadata-service"},
    {"event": "HIDE_LOADER", "source": "NEW_TAB", "value": 6000, "action": "activity_stream_masga_event", "tab_id": "-3-2", "client_id": "a7967bc5-38ea-dd48-bfe9-ee06ca94f7e1", "addon_version": "1.1.8", "locale": "en-US", "page": "NEW_TAB", "session_id": "{d8a1812e-9f38-184c-9eed-01b98d4363e5}", "experiment_id": "exp-005-metadata-service"},
    {"session_duration": (2 ** 31 + 950), "locale": "en-US", "ip": "15.211.153.0", "date": "2016-04-04", "unload_reason": "close", "client_id": "93a7579d-c986-4e33-809e-e4101bf523f9", "max_scroll_depth": 61, "addon_version": "1.0.5", "total_history_size": 460, "ver": "3", "ua": "python-requests\/2.9.1", "load_latency": 216, "click_position": 19, "timestamp": 1459810810000, "action": "activity_stream_session", "tab_id": "5", "load_reason": "focus", "page": "timeline", "total_bookmarks": 3},
    {"locale": "en-US", "ip": "15.211.153.0", "client_id": "1249e986-b53f-4851-8f77-a9c87f8f6646", "date": "2016-04-04", "event": "previewCacheFetch", "event_id": "fd12fda24xd15", "addon_version": "1.0.5", "ver": "3", "source": "recent_links", "timestamp": 1459810810000, "action": "activity_stream_performance", "tab_id": "4", "ua": "python-requests\/2.9.1", "value": 2 ** 31 + 25},
]


class TestActivityStream(unittest.TestCase):
    def setUp(self):
        self.params = {}
        super(TestActivityStream, self).setUp()

    def test_filters(self):
        n_app_logs = 0
        n_session_logs = 0
        n_event_logs = 0
        n_performance_logs = 0
        n_masga_logs = 0
        n_ss_session_logs = 0
        n_ss_event_logs = 0
        n_ss_performance_logs = 0
        n_ss_masga_logs = 0

        for line in FIXTURE:
            for _ in application_stats_filter(line, self.params):
                n_app_logs += 1

            for _ in activity_stream_session_filter(line, self.params):
                n_session_logs += 1

            for _ in activity_stream_event_filter(line, self.params):
                n_event_logs += 1

            for _ in activity_stream_performance_filter(line, self.params):
                n_performance_logs += 1

            for _ in activity_stream_masga_filter(line, self.params):
                n_masga_logs += 1

            # test the shield study filters
            line["shield_variant"] = "test"
            for _ in ss_activity_stream_session_filter(line, self.params):
                n_ss_session_logs += 1

            for _ in ss_activity_stream_event_filter(line, self.params):
                n_ss_event_logs += 1

            for _ in ss_activity_stream_performance_filter(line, self.params):
                n_ss_performance_logs += 1

            for _ in ss_activity_stream_masga_filter(line, self.params):
                n_ss_masga_logs += 1

        self.assertEqual(n_app_logs, 5)
        self.assertEqual(n_session_logs, 6)
        self.assertEqual(n_event_logs, 5)
        self.assertEqual(n_performance_logs, 6)
        self.assertEqual(n_masga_logs, 5)
        self.assertEqual(n_ss_session_logs, 6)
        self.assertEqual(n_ss_event_logs, 5)
        self.assertEqual(n_ss_performance_logs, 6)
        self.assertEqual(n_ss_masga_logs, 5)

        # test filters are mutually orthogonal
        n_total = 0
        for f1, f2 in combinations([activity_stream_event_filter,
                                    activity_stream_session_filter,
                                    activity_stream_performance_filter,
                                    application_stats_filter,
                                    activity_stream_masga_filter,
                                    ss_activity_stream_session_filter,
                                    ss_activity_stream_event_filter,
                                    ss_activity_stream_performance_filter,
                                    ss_activity_stream_masga_filter], 2):
            for line in FIXTURE:
                for item in f1(line, self.params):
                        for _ in f2(item, self.params):
                            n_total += 1
        self.assertEqual(n_total, 0)

    def test_clean_activity_stream_session(self):
        self.assertIsNotNone(clean_activity_stream_session(FIXTURE[0], self.params).next())

        ret = clean_activity_stream_session(FIXTURE[-2], self.params)
        self.assertRaises(StopIteration, ret.next)

        # test the filter on the required fields
        for field_name in ["client_id", "tab_id", "addon_version", "page",
                           "load_reason", "unload_reason", "session_duration"]:
            line = FIXTURE[0].copy()
            del line[field_name]
            ret = clean_activity_stream_session(line, self.params)
            self.assertRaises(StopIteration, ret.next)

        # test the filter on the optional fields
        for field_name in ["load_latency", "experiment_id", "total_bookmarks",
                           "total_history_size", "session_id", "highlights_size",
                           "max_scroll_depth"]:
            line = FIXTURE[0].copy()
            del line[field_name]
            self.assertIsNotNone(clean_activity_stream_session(line, self.params).next())

        # test the filter on the numeric fields with invalid values
        for field_name in ["session_duration", "total_bookmarks", "total_history_size",
                           "highlights_size", "max_scroll_depth"]:
            line = FIXTURE[0].copy()
            line[field_name] = -1000
            ret = clean_activity_stream_session(line, self.params)
            self.assertRaises(StopIteration, ret.next)

    def test_clean_activity_stream_event(self):
        self.assertIsNotNone(clean_activity_stream_event(FIXTURE[5], self.params).next())

        # test the filter on the required fields
        for field_name in ["client_id", "tab_id", "addon_version", "page", "event"]:
            line = FIXTURE[5].copy()
            del line[field_name]
            ret = clean_activity_stream_event(line, self.params)
            self.assertRaises(StopIteration, ret.next)

        # test the filter on the optional fields
        for field_name in ['action_position', 'source', 'experiment_id',
                           'session_id', 'url', 'recommender_type',
                           'highlight_type', 'provider', 'metadata_source']:
            line = FIXTURE[5].copy()
            del line[field_name]
            self.assertIsNotNone(clean_activity_stream_event(line, self.params).next())

    def test_clean_activity_stream_performance(self):
        self.assertIsNotNone(clean_activity_stream_performance(FIXTURE[10], self.params).next())

        ret = clean_activity_stream_performance(FIXTURE[-1], self.params)
        self.assertRaises(StopIteration, ret.next)

        # test the filter on the required fields
        for field_name in ["client_id", "tab_id", "addon_version",
                           "event", "event_id", "source", "value"]:
            line = FIXTURE[10].copy()
            del line[field_name]
            ret = clean_activity_stream_performance(line, self.params)
            self.assertRaises(StopIteration, ret.next)

        # test the filter on the optional fields
        for field_name in ["session_id", "experiment_id", "metadata_source"]:
            line = FIXTURE[10].copy()
            del line[field_name]
            self.assertIsNotNone(clean_activity_stream_performance(line, self.params).next())

        # test the filter on the numeric fields with invalid values
        for field_name in ["value"]:
            line = FIXTURE[10].copy()
            line[field_name] = -1000
            ret = clean_activity_stream_performance(line, self.params)
            self.assertRaises(StopIteration, ret.next)

        # test the filter on the numeric fields with float
        for field_name in ["value"]:
            line = FIXTURE[10].copy()
            line[field_name] = 100.4
            ret = clean_activity_stream_performance(line, self.params)
            self.assertEquals(ret.next()["value"], 100)

    def test_clean_activity_stream_masga(self):
        self.assertIsNotNone(clean_activity_stream_masga(FIXTURE[20], self.params).next())

        # test the filter on the required fields
        for field_name in ["client_id", "tab_id", "addon_version",
                           "event", "source", "value"]:
            line = FIXTURE[20].copy()
            del line[field_name]
            ret = clean_activity_stream_masga(line, self.params)
            self.assertRaises(StopIteration, ret.next)

        # test the filter on the optional fields
        for field_name in ["session_id", "experiment_id"]:
            line = FIXTURE[20].copy()
            del line[field_name]
            self.assertIsNotNone(clean_activity_stream_masga(line, self.params).next())

        # test the filter on the numeric fields with invalid values
        for field_name in ["value"]:
            line = FIXTURE[20].copy()
            line[field_name] = 2 ** 32 + 1
            ret = clean_activity_stream_masga(line, self.params)
            self.assertEqual(ret.next()["value"], -1)

    def test_clean_shield_study_fields(self):
        self.assertIsNotNone(clean_shield_study_fields(FIXTURE[0], self.params).next())

        line = FIXTURE[0].copy()
        line["tp_version"] = "1.0.0"
        self.assertIsNotNone(clean_shield_study_fields(line, self.params).next())
