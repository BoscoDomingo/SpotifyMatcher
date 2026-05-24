import unittest
from unittest.mock import Mock

import main


class TestMain(unittest.TestCase):
    def test_get_user_data_with_username_only(self):
        username, playlist_id = main.get_user_data(["main.py", "alice"])
        self.assertEqual(username, "alice")
        self.assertEqual(playlist_id, "")

    def test_get_user_data_with_playlist(self):
        username, playlist_id = main.get_user_data(["main.py", "alice", "playlist123"])
        self.assertEqual(username, "alice")
        self.assertEqual(playlist_id, "playlist123")

    def test_calculate_success_rate(self):
        self.assertEqual(main.calculate_success_rate(25, 40), "62.50")
        self.assertEqual(main.calculate_success_rate(0, 0), "0.00")

    def test_add_tracks_to_playlist_batches(self):
        sp = Mock()
        track_ids = [f"id{i}" for i in range(205)]

        main.add_tracks_to_playlist(sp, "alice", "playlist123", track_ids)

        self.assertEqual(sp.user_playlist_add_tracks.call_count, 3)
        self.assertEqual(track_ids, [])


if __name__ == "__main__":
    unittest.main()
