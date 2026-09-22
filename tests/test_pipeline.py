import unittest

from kim_holiday.pipeline import ContentDraftPipeline, DraftRejected


class ContentDraftPipelineTests(unittest.TestCase):
    def test_produces_approval_gated_validated_draft(self):
        draft = ContentDraftPipeline().run("questions to ask before planning")
        self.assertEqual(draft["status"], "draft")
        self.assertTrue(draft["approval_required"])
        self.assertEqual(draft["review"]["anti_slop"], "passed")
        self.assertIn("Kim Holiday", draft["caption"])
        self.assertIn("Kirim DM", draft["caption"])
        self.assertNotIn("Planning something special", draft["caption"])
        self.assertIn("visual_direction", draft)

    def test_rejects_empty_topic(self):
        with self.assertRaises(DraftRejected):
            ContentDraftPipeline().run(" ")

    def test_rejects_unsupported_claims(self):
        pipeline = ContentDraftPipeline()
        draft = pipeline._brand_guard(
            {
                "channel": "Instagram",
                "topic": "x",
                "caption": "Kim Holiday is available today for $99.",
                "cta": "DM Kim Holiday.",
                "visual_direction": "Visual sederhana.",
            },
            {"angle": "x"},
        )
        with self.assertRaises(DraftRejected):
            pipeline._anti_slop_review(draft)
