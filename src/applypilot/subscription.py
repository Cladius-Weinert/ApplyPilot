"""Subscription/pricing catalog for product planning.

This module intentionally does not process payments or authorize hosted SaaS
access. It is a public product/pricing catalog that keeps the project
subscription-ready without adding a billing backend before it is needed.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

PlanId = Literal["free", "starter", "pro", "agency"]


@dataclass(frozen=True)
class FeatureLimits:
    daily_job_lead_limit: int
    max_profiles: int
    export_enabled: bool = False
    portfolio_builder_enabled: bool = False
    premium_prompts_enabled: bool = False
    saved_searches_enabled: bool = False
    match_scoring_enabled: bool = False
    cv_cover_suggestions_enabled: bool = False
    resume_tailoring_enabled: bool = False
    rws_aop_templates_enabled: bool = False
    freelance_gig_generator_enabled: bool = False
    priority_scoring_enabled: bool = False
    team_notes_enabled: bool = False
    reusable_templates_enabled: bool = False
    reports_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__.copy()


@dataclass(frozen=True)
class SubscriptionPlan:
    plan_id: PlanId
    plan_name: str
    monthly_price_placeholder: str
    feature_limits: FeatureLimits
    included_features: tuple[str, ...]
    cta: str


PLANS: dict[PlanId, SubscriptionPlan] = {
    "free": SubscriptionPlan(
        plan_id="free",
        plan_name="Free",
        monthly_price_placeholder="$0/mo",
        feature_limits=FeatureLimits(daily_job_lead_limit=5, max_profiles=1),
        included_features=(
            "5 job leads per day",
            "Basic application tracker",
            "Basic CV template",
            "Basic cover letter template",
            "Manual job board checklist",
        ),
        cta="Start free",
    ),
    "starter": SubscriptionPlan(
        plan_id="starter",
        plan_name="Starter",
        monthly_price_placeholder="$19/mo placeholder",
        feature_limits=FeatureLimits(
            daily_job_lead_limit=25,
            max_profiles=1,
            export_enabled=True,
            saved_searches_enabled=True,
            match_scoring_enabled=True,
            cv_cover_suggestions_enabled=True,
        ),
        included_features=(
            "Saved job search queries",
            "Job match scoring",
            "CV and cover letter suggestions",
            "Daily job discovery workflow",
            "CSV export",
            "14-day income sprint plan",
        ),
        cta="Choose Starter",
    ),
    "pro": SubscriptionPlan(
        plan_id="pro",
        plan_name="Pro",
        monthly_price_placeholder="$49/mo placeholder",
        feature_limits=FeatureLimits(
            daily_job_lead_limit=100,
            max_profiles=1,
            export_enabled=True,
            saved_searches_enabled=True,
            match_scoring_enabled=True,
            cv_cover_suggestions_enabled=True,
            portfolio_builder_enabled=True,
            premium_prompts_enabled=True,
            resume_tailoring_enabled=True,
            rws_aop_templates_enabled=True,
            freelance_gig_generator_enabled=True,
            priority_scoring_enabled=True,
        ),
        included_features=(
            "AI evaluator portfolio builder",
            "Premium prompt library",
            "Resume tailoring workflow",
            "RWS/AOP research workflow templates",
            "Freelance gig generator",
            "Priority scoring for Mercor, Outlier, TELUS, Mindrift, OneForma, RWS, Prolific",
        ),
        cta="Choose Pro",
    ),
    "agency": SubscriptionPlan(
        plan_id="agency",
        plan_name="Agency",
        monthly_price_placeholder="$149/mo placeholder",
        feature_limits=FeatureLimits(
            daily_job_lead_limit=500,
            max_profiles=25,
            export_enabled=True,
            saved_searches_enabled=True,
            match_scoring_enabled=True,
            cv_cover_suggestions_enabled=True,
            portfolio_builder_enabled=True,
            premium_prompts_enabled=True,
            resume_tailoring_enabled=True,
            rws_aop_templates_enabled=True,
            freelance_gig_generator_enabled=True,
            priority_scoring_enabled=True,
            team_notes_enabled=True,
            reusable_templates_enabled=True,
            reports_enabled=True,
        ),
        included_features=(
            "Multiple profiles",
            "Client/application pipelines",
            "Reusable templates",
            "Team notes",
            "Export reports",
        ),
        cta="Contact for Agency",
    ),
}


def get_plan(plan_id: str | None) -> SubscriptionPlan:
    normalized = (plan_id or "free").strip().lower()
    return PLANS.get(normalized, PLANS["free"])  # type: ignore[arg-type]
