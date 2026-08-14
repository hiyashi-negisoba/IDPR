from idpr.v2.deterministic_interactions import explicit_conspiracy_interactions


def test_explicit_conspiracy_recovers_participants_not_incidental_victim() -> None:
    text = (
        "A군의 군수인 甲은 사채업자인 乙과 공모하여 관내 건설업자 丙에게 "
        "금전적 지원을 요구하기로 마음먹었다."
    )
    assert explicit_conspiracy_interactions(
        episode_source_quotes=[text],
        episode_participant_ids=["甲", "乙", "丙"],
        responsibility_actor_ids=["甲", "乙", "丙"],
    ) == [
        {
            "interaction_type": "agreement_or_coordinated_conduct",
            "source_actor_id": "甲",
            "target_actor_ids": ["乙"],
            "evidence_quotes": [
                (
                    "甲은 사채업자인 乙과 공모하여 관내 건설업자 丙에게 "
                    "금전적 지원을 요구하기로 마음먹었다."
                )
            ],
        }
    ]


def test_explicit_conspiracy_ignores_actor_outside_responsibility() -> None:
    assert explicit_conspiracy_interactions(
        episode_source_quotes=["A는 乙과 공모하여 절취하기로 마음먹었다."],
        episode_participant_ids=["A", "乙"],
        responsibility_actor_ids=["乙"],
    ) == []


def test_explicit_joint_plan_formula_is_recovered() -> None:
    assert explicit_conspiracy_interactions(
        episode_source_quotes=["甲과 乙은 한 건 하기로 하고 ATM 앞을 서성댔다."],
        episode_participant_ids=["甲", "乙"],
        responsibility_actor_ids=["甲", "乙"],
    ) == [
        {
            "interaction_type": "agreement_or_coordinated_conduct",
            "source_actor_id": "甲",
            "target_actor_ids": ["乙"],
            "evidence_quotes": ["甲과 乙은 한 건 하기로"],
        }
    ]
