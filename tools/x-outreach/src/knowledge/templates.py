"""Reply and DM template management.

Templates are organised by classification category (A-G for replies,
A-E for DMs) with rotation tracking to avoid sending identical messages.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field


@dataclass
class Template:
    """A single message template with placeholders."""

    id: str
    category: str
    text: str
    use_count: int = 0


# ---------------------------------------------------------------------------
# Reply templates (categories A-G from strategy docs)
# ---------------------------------------------------------------------------

REPLY_TEMPLATES: dict[str, list[Template]] = {
    "A": [
        # Positive experience
        Template(
            id="A1",
            category="A",
            text=(
                "いいなあ！仕上がりめっちゃ自然だね。ちなみにそのクリニック、"
                "カウンセリングって日本語でできた？"
            ),
        ),
        Template(
            id="A2",
            category="A",
            text=(
                "これは良い結果！同じ施術でも場所によって結構違うから、"
                "いいとこ見つけたね。ダウンタイムどのくらいだった？"
            ),
        ),
    ],
    "B": [
        # Questions / concerns
        Template(
            id="B1",
            category="B",
            text=(
                "クリニック選び悩むよね。個人的に調べてて思うのは"
                "「外国人患者誘致医療機関」登録の有無と日本語対応のレベル"
                "をまず確認するのが大事。この2つだけでもかなり絞れるよ"
            ),
        ),
        Template(
            id="B2",
            category="B",
            text=(
                "いま韓国の皮膚科データ調べてるんだけど、同じ施術でも"
                "クリニックで最大数倍の価格差あるから、まず施術を決めてから"
                "エリアで絞るのがおすすめ"
            ),
        ),
    ],
    "C": [
        # Price sharing
        Template(
            id="C1",
            category="C",
            text=(
                "お、いい価格帯！ちなみにその料金は製剤何使ってるか聞いた？"
                "韓国製とアラガンで相場が結構変わるんだよね"
            ),
        ),
    ],
    "D": [
        # Trouble / failure
        Template(
            id="D1",
            category="D",
            text=(
                "読んでてつらい…本当に大変だったね。韓国のクリニックが"
                "「外国人患者誘致医療機関」登録してたら対応義務があるから、"
                "まだ対応求められるかも。確認してみて"
            ),
        ),
    ],
    "E": [
        # Planning / preparation
        Template(
            id="E1",
            category="E",
            text=(
                "初渡韓美容たのしみだね！もし施術決まってるなら、"
                "同じエリアの他クリニックの相場もざっくり把握しておくと安心だよ。"
                "何受ける予定？"
            ),
        ),
    ],
    "F": [
        # Clinic official (usually do not reply)
        Template(
            id="F1",
            category="F",
            text="",  # Intentionally empty -- skip replies to clinic accounts
        ),
    ],
    "G": [
        # Before/after progress
        Template(
            id="G1",
            category="G",
            text=(
                "1週間でこの変化すごい！はっきり見える。"
                "これって何回目の施術？"
            ),
        ),
    ],
}


# ---------------------------------------------------------------------------
# DM templates (A-E from strategy docs) -- M2 stubs
# ---------------------------------------------------------------------------

DM_TEMPLATES: dict[str, list[Template]] = {
    "A": [
        Template(
            id="DM_A1",
            category="A",
            text=(
                "{施術名}の投稿見て気になってDMしちゃった！"
                "{具体的な感想}ってあったけど、実際受けてみてクリニック探すの大変だった？\n\n"
                "じつは韓国の皮膚科クリニックの料金とか施術データ集めてまとめてるんだけど、"
                "実際に行った人の声がいちばん参考になるなって思って。\n\n"
                "よかったらクリニックどうやって見つけたか教えてほしいな"
            ),
        ),
    ],
    "B": [
        Template(
            id="DM_B1",
            category="B",
            text=(
                "ビフォーアフターすごい！{具体的な変化}。\n\n"
                "ちょっと聞きたいんだけど、このクリニックって何で知った？"
                "ネットで調べた？それとも誰かの紹介？\n\n"
                "いま韓国の皮膚科の料金比較データまとめてて、"
                "探し方のリアルが知りたくて。迷惑じゃなければ教えてほしい"
            ),
        ),
    ],
    "C": [
        Template(
            id="DM_C1",
            category="C",
            text=(
                "クリニック選びの投稿めっちゃわかる！{相手の悩みへの共感}\n\n"
                "じつは自分も韓国の皮膚科データずっと調べてて、"
                "クリニック選びって本当に情報少ないなって感じてる。"
                "いま料金比較とかまとめてるんだけど、結局どうやって決めた？\n\n"
                "いちばん困ったこととか教えてもらえたらめちゃ助かる"
            ),
        ),
    ],
    "D": [
        Template(
            id="DM_D1",
            category="D",
            text=(
                "料金の話すごく気になった！{相手の投稿内容}\n\n"
                "韓国の皮膚科って「安い」って言われてるけど、"
                "実際クリニックによってかなり差あるんだよね。"
                "いまそのデータ集めてて比較サイト作ろうとしてるんだけど、"
                "料金って事前にどうやって調べた？\n\n"
                "比較する方法あったのか気になって"
            ),
        ),
    ],
    "E": [
        Template(
            id="DM_E1",
            category="E",
            text=(
                "初の渡韓美容おつかれさま！{投稿の感想への反応}\n\n"
                "初めてだと色々わからないこと多かったんじゃない？"
                "自分は韓国の皮膚科情報を調べてまとめてる人なんだけど、"
                "行く前にいちばん不安だったこととか、"
                "「これ先に知りたかった」ってことあったら聞きたいな\n\n"
                "今後行く人の参考にできたらいいなと思って"
            ),
        ),
    ],
}


class TemplateSelector:
    """Select and rotate templates to avoid repetition.

    Tracks usage counts per template and picks the least-used one in
    each category to ensure even rotation.
    """

    def __init__(self) -> None:
        self._reply_templates = REPLY_TEMPLATES
        self._dm_templates = DM_TEMPLATES
        self._last_reply_id: str | None = None
        self._last_dm_id: str | None = None

    def get_reply_template(self, category: str) -> Template | None:
        """Pick the least-used reply template for *category*.

        Returns ``None`` if the category has no templates or the
        template text is empty (e.g. category F -- clinic accounts).
        """
        templates = self._reply_templates.get(category, [])
        if not templates:
            return None

        # Filter out empty templates
        usable = [t for t in templates if t.text]
        if not usable:
            return None

        # Pick least used, breaking ties randomly
        min_count = min(t.use_count for t in usable)
        candidates = [t for t in usable if t.use_count == min_count]

        # Avoid repeating the same template consecutively
        if len(candidates) > 1 and self._last_reply_id:
            candidates = [c for c in candidates if c.id != self._last_reply_id] or candidates

        chosen = random.choice(candidates)
        chosen.use_count += 1
        self._last_reply_id = chosen.id
        return chosen

    def get_dm_template(self, category: str) -> Template | None:
        """Pick the least-used DM template for *category*."""
        templates = self._dm_templates.get(category, [])
        if not templates:
            return None

        min_count = min(t.use_count for t in templates)
        candidates = [t for t in templates if t.use_count == min_count]

        if len(candidates) > 1 and self._last_dm_id:
            candidates = [c for c in candidates if c.id != self._last_dm_id] or candidates

        chosen = random.choice(candidates)
        chosen.use_count += 1
        self._last_dm_id = chosen.id
        return chosen

    def get_categories(self, template_type: str = "reply") -> list[str]:
        """Return available category keys for reply or DM templates."""
        if template_type == "dm":
            return list(self._dm_templates.keys())
        return list(self._reply_templates.keys())
