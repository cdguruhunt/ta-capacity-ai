import math
from app.models.calculation import WorkforceInput, TAStructureResult


COMPLEXITY_MAP = {
    "low": 1.0,
    "medium": 1.1,
    "high": 1.2,
    "hyper": 1.4,
}

VOLUME_MAP = {
    "low": 1.0,
    "medium": 1.1,
    "high": 1.2,
    "hyper": 1.25,
}

GEOGRAPHY_MULTIPLIER = {
    "domestic": 1.0,
    "multi-region": 1.1,
    "global": 1.25,
}

AVG_SALARY_MAP = {
    "product": 1_800_000,
    "gcc": 1_600_000,
    "startup": 1_400_000,
    "enterprise": 1_500_000,
    "consulting": 1_200_000,
}


def _ceil(x: float) -> int:
    return math.ceil(x)


def calculate_ta_structure(inputs: WorkforceInput) -> TAStructureResult:
    # Step 1: Dropout adjustment
    adjusted_hiring = _ceil(inputs.hiring_target / (1 - inputs.dropout_ratio / 100))

    # Geography multiplier
    geo_mult = GEOGRAPHY_MULTIPLIER.get(inputs.geography, 1.0)

    # AI/Niche boost
    ai_boost = 1 + (inputs.ai_niche_percent / 100) * 0.3

    company = inputs.company_type

    if company in ("product", "gcc", "startup"):
        cf = COMPLEXITY_MAP[inputs.complexity_factor]
        productivity = inputs.recruiter_productivity
        core_recruiters = _ceil((adjusted_hiring * cf * ai_boost * geo_mult) / productivity)

        junior_recruiters = round(core_recruiters * 0.40)
        recruiters = round(core_recruiters * 0.35)
        senior_recruiters = round(core_recruiters * 0.25)
        sourcers = _ceil(core_recruiters / 4)
        coordinators = _ceil(core_recruiters / 7)
        leads = _ceil(core_recruiters / 5)
        managers = _ceil(leads / 3)
        ta_head = 1

        model_used = "Product / Niche Complexity Model"

    else:  # consulting, enterprise
        vf = VOLUME_MAP[inputs.complexity_factor]
        if company == "enterprise":
            productivity = min(inputs.recruiter_productivity, 45)
        else:
            productivity = min(inputs.recruiter_productivity, 55)

        core_recruiters = _ceil((adjusted_hiring * vf * geo_mult) / productivity)

        junior_recruiters = round(core_recruiters * 0.50)
        recruiters = round(core_recruiters * 0.35)
        senior_recruiters = round(core_recruiters * 0.15)
        sourcers = _ceil(core_recruiters / 5)
        coordinators = _ceil(core_recruiters / 8)
        leads = _ceil(core_recruiters / 6)
        managers = _ceil(leads / 3)
        ta_head = 1

        model_used = "Volume / Consulting Model"

    total_ta = (junior_recruiters + recruiters + senior_recruiters +
                sourcers + coordinators + leads + managers + ta_head)

    hiring_capacity = round(core_recruiters * productivity)
    utilization = min(98.0, round((adjusted_hiring / max(hiring_capacity, 1)) * 100, 1))

    months = _ceil(adjusted_hiring / max(core_recruiters * (productivity / 12), 1))
    timeline = f"{months}–{months + 2} months"

    avg_salary = AVG_SALARY_MAP.get(company, 1_400_000)
    total_cost = total_ta * avg_salary
    cost_per_hire = round(total_cost / max(inputs.hiring_target, 1))

    estimated_cost = f"₹{total_cost / 100_000:.1f}L/yr"
    cost_per_hire_str = f"₹{cost_per_hire:,}"

    return TAStructureResult(
        adjusted_hiring=adjusted_hiring,
        total_ta=total_ta,
        junior_recruiters=junior_recruiters,
        recruiters=recruiters,
        senior_recruiters=senior_recruiters,
        sourcers=sourcers,
        coordinators=coordinators,
        leads=leads,
        managers=managers,
        ta_head=ta_head,
        hiring_capacity=hiring_capacity,
        timeline=timeline,
        utilization=utilization,
        estimated_cost=estimated_cost,
        cost_per_hire=cost_per_hire_str,
        model_used=model_used,
    )
