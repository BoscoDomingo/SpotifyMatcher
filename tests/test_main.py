import unittest
from contextlib import redirect_stdout
from io import StringIO
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

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

    def test_run_reuses_spotify_searches_for_duplicate_songs(self):
        sp = Mock()
        sp.search.side_effect = [
            {"tracks": {"items": [{"id": "warmup"}]}},
            {"tracks": {"items": [{"id": "track123"}]}},
        ]
        auth_manager = Mock()
        auth_manager.is_token_expired.return_value = False

        with TemporaryDirectory() as tmpdir:
            failed_matches_filename = f"{tmpdir}/failed.txt"

            with (
                patch("main.get_user_data", return_value=("alice", "playlist123")),
                patch("main.connect_to_spotify", return_value=(sp, auth_manager)),
                patch("main.get_auth_token", return_value={"refresh_token": "refresh"}),
                patch(
                    "main.get_title_and_artist",
                    return_value=[
                        ("track:Song artist:Artist", "Artist - Song"),
                        ("track:Song artist:Artist", "Artist - Song"),
                    ],
                ),
                patch("main.ensure_playlist_exists", return_value="playlist123"),
                patch("main.FAILED_MATCHES_FILENAME", failed_matches_filename),
            ):
                with redirect_stdout(StringIO()):
                    main.run()

            sp.user_playlist_add_tracks.assert_called_once_with(
                "alice",
                "playlist123",
                ["track123", "track123"],
            )
            self.assertEqual(sp.search.call_count, 2)

            with open(failed_matches_filename, encoding="utf-8") as failed_matches_file:
                self.assertEqual(failed_matches_file.read(), "")


if __name__ == "__main__":
    unittest.main()
