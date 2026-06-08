"""
Shared crop knowledge base used by the calendar, recommendation and profit
features. Values are practical approximations for North-India (Punjab) farming
and are clearly treated as guidance, not guarantees.
"""
from __future__ import annotations

# season: which sowing window the crop belongs to.
#   kharif  ~ Jun-Jul (monsoon)   rabi ~ Oct-Nov (winter)
# yield_q_per_acre: typical yield in quintals/acre
# cost_per_acre: typical input cost (seed+fertilizer+labour) in INR
# duration_days: sowing -> harvest
CROPS: dict[str, dict] = {
    "Wheat": {
        "season": "rabi",
        "ideal_ph": (6.0, 7.5),
        "n_need": "high",
        "yield_q_per_acre": 20,
        "cost_per_acre": 18000,
        "duration_days": 140,
        "schedule": [
            (0, "Sowing - use certified seed, treat with fungicide."),
            (21, "First irrigation (Crown Root Initiation stage)."),
            (25, "First top-dose of Urea after irrigation."),
            (45, "Second irrigation; scout for weeds."),
            (65, "Third irrigation (tillering/jointing)."),
            (90, "Irrigation at flowering - critical for grain set."),
            (115, "Irrigation at grain-filling."),
            (140, "Harvest when grains are hard and golden."),
        ],
    },
    "Paddy": {
        "season": "kharif",
        "ideal_ph": (5.5, 7.0),
        "n_need": "high",
        "yield_q_per_acre": 25,
        "cost_per_acre": 22000,
        "duration_days": 120,
        "schedule": [
            (0, "Transplant 25-30 day old seedlings into puddled field."),
            (15, "Maintain 2-5 cm standing water; first Urea dose."),
            (30, "Weed control; second Urea dose at tillering."),
            (55, "Third Urea dose at panicle initiation."),
            (75, "Keep water at flowering - do not let field dry."),
            (110, "Drain field 10 days before harvest."),
            (120, "Harvest at 80% grain maturity."),
        ],
    },
    "Maize": {
        "season": "kharif",
        "ideal_ph": (5.5, 7.5),
        "n_need": "high",
        "yield_q_per_acre": 22,
        "cost_per_acre": 16000,
        "duration_days": 100,
        "schedule": [
            (0, "Sowing - maintain row spacing 60 cm."),
            (20, "First Urea top-dose; remove weeds."),
            (40, "Second Urea dose at knee-high stage."),
            (55, "Irrigation at tasseling - critical stage."),
            (70, "Irrigation at grain filling."),
            (100, "Harvest when husks dry and kernels hard."),
        ],
    },
    "Cotton": {
        "season": "kharif",
        "ideal_ph": (6.0, 8.0),
        "n_need": "medium",
        "yield_q_per_acre": 10,
        "cost_per_acre": 25000,
        "duration_days": 170,
        "schedule": [
            (0, "Sowing - use Bt cotton certified seed."),
            (30, "Thinning + first fertilizer dose; scout for sucking pests."),
            (60, "Square formation - monitor for bollworm, set pheromone traps."),
            (90, "Flowering - ensure adequate moisture."),
            (120, "Boll development - continue pest scouting."),
            (150, "First picking of mature bolls."),
            (170, "Final picking."),
        ],
    },
    "Mustard": {
        "season": "rabi",
        "ideal_ph": (6.0, 7.5),
        "n_need": "medium",
        "yield_q_per_acre": 8,
        "cost_per_acre": 9000,
        "duration_days": 130,
        "schedule": [
            (0, "Sowing - shallow, well-prepared seedbed."),
            (25, "First irrigation + Urea top-dose; thin plants."),
            (50, "Scout for aphids (major mustard pest)."),
            (70, "Irrigation at flowering."),
            (100, "Irrigation at pod formation."),
            (130, "Harvest when pods turn yellow-brown."),
        ],
    },
    "Sugarcane": {
        "season": "kharif",
        "ideal_ph": (6.0, 7.5),
        "n_need": "high",
        "yield_q_per_acre": 350,
        "cost_per_acre": 35000,
        "duration_days": 330,
        "schedule": [
            (0, "Planting setts in furrows."),
            (35, "First irrigation + Nitrogen dose; gap filling."),
            (90, "Earthing up + second Nitrogen dose."),
            (150, "Tying of canes; monitor borers."),
            (240, "Reduce irrigation as crop matures."),
            (330, "Harvest at full maturity."),
        ],
    },
}


def crop_list() -> list[str]:
    return list(CROPS.keys())
