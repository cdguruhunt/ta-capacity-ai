from typing import Dict, Any


BENCHMARKS: Dict[str, Any] = {
    "product": {
        "company_type": "IT Product Company",
        "avg_recruiter_productivity": {"min": 25, "max": 38, "median": 32},
        "typical_dropout_ratio": {"min": 20, "max": 35, "median": 25},
        "sourcer_ratio": "1 sourcer per 3–4 recruiters",
        "coordinator_ratio": "1 coordinator per 6–8 recruiters",
        "avg_time_to_fill_days": {"junior": 30, "mid": 50, "senior": 75, "niche": 90},
        "typical_team_size_per_100_hires": 5,
        "cost_per_hire_inr": {"min": 35000, "max": 120000},
        "notes": "Niche/AI roles add 25–40% recruiter load. Passive sourcing required.",
        "benchmarks_source": "Naukri Hiring Intelligence 2024, LinkedIn India Talent Trends",
    },
    "consulting": {
        "company_type": "IT Consulting Company",
        "avg_recruiter_productivity": {"min": 45, "max": 65, "median": 55},
        "typical_dropout_ratio": {"min": 15, "max": 25, "median": 18},
        "sourcer_ratio": "1 sourcer per 5 recruiters",
        "coordinator_ratio": "1 coordinator per 8–10 recruiters",
        "avg_time_to_fill_days": {"junior": 15, "mid": 25, "senior": 45, "niche": 60},
        "typical_team_size_per_100_hires": 3,
        "cost_per_hire_inr": {"min": 15000, "max": 50000},
        "notes": "Volume-driven. Repeat skills. Vendor-heavy. Fast turnaround.",
        "benchmarks_source": "Naukri Hiring Intelligence 2024",
    },
    "gcc": {
        "company_type": "Global Capability Center",
        "avg_recruiter_productivity": {"min": 28, "max": 42, "median": 35},
        "typical_dropout_ratio": {"min": 22, "max": 35, "median": 28},
        "sourcer_ratio": "1 sourcer per 3–5 recruiters",
        "coordinator_ratio": "1 coordinator per 7 recruiters",
        "avg_time_to_fill_days": {"junior": 35, "mid": 55, "senior": 80, "niche": 95},
        "typical_team_size_per_100_hires": 4,
        "cost_per_hire_inr": {"min": 40000, "max": 140000},
        "notes": "Mix of niche tech and volume lateral hiring. Global coordination overhead.",
        "benchmarks_source": "NASSCOM GCC Talent Report 2024",
    },
    "startup": {
        "company_type": "Startup",
        "avg_recruiter_productivity": {"min": 20, "max": 35, "median": 28},
        "typical_dropout_ratio": {"min": 25, "max": 45, "median": 30},
        "sourcer_ratio": "1 sourcer per 3 recruiters",
        "coordinator_ratio": "1 coordinator per 5 recruiters",
        "avg_time_to_fill_days": {"junior": 20, "mid": 40, "senior": 70, "niche": 100},
        "typical_team_size_per_100_hires": 5,
        "cost_per_hire_inr": {"min": 25000, "max": 90000},
        "notes": "High dropout due to competitor offers. Brand and comp matters. Lean team.",
        "benchmarks_source": "Inc42 India Startup Hiring Report 2024",
    },
    "enterprise": {
        "company_type": "Enterprise",
        "avg_recruiter_productivity": {"min": 35, "max": 50, "median": 42},
        "typical_dropout_ratio": {"min": 15, "max": 25, "median": 18},
        "sourcer_ratio": "1 sourcer per 5–6 recruiters",
        "coordinator_ratio": "1 coordinator per 8 recruiters",
        "avg_time_to_fill_days": {"junior": 25, "mid": 40, "senior": 65, "niche": 85},
        "typical_team_size_per_100_hires": 3,
        "cost_per_hire_inr": {"min": 20000, "max": 80000},
        "notes": "Structured processes. Strong employer brand. Multiple approvals.",
        "benchmarks_source": "Mercer India TA Benchmarks 2024",
    },
}


def get_benchmarks(company_type: str) -> Dict[str, Any]:
    """Return benchmark data for a given company type."""
    ct = company_type.lower()
    if ct not in BENCHMARKS:
        available = list(BENCHMARKS.keys())
        raise ValueError(f"Company type '{company_type}' not found. Available: {available}")
    return BENCHMARKS[ct]
