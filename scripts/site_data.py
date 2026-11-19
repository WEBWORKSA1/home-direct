# -*- coding: utf-8 -*-
"""Shared data for Home.Direct: services, maintenance calendar, contest themes, ROI projects, roles."""

SERVICES = [
  ("Exterior", [("roofing", "Roofing"), ("siding", "Siding"), ("windows", "Windows & doors"), ("gutters", "Gutters"), ("painting", "Painting (interior or exterior)"), ("garage-doors", "Garage doors"), ("concrete", "Concrete & driveways")]),
  ("Systems", [("hvac", "Heating & cooling (HVAC)"), ("plumbing", "Plumbing & water heaters"), ("electrical", "Electrical & panels"), ("solar", "Solar & batteries"), ("insulation", "Insulation & air sealing")]),
  ("Interior", [("remodeling", "Kitchen, bath & basement remodeling"), ("flooring", "Flooring"), ("handyman", "Handyman & small repairs"), ("cleaning", "Cleaning")]),
  ("Repair & restoration", [("foundation", "Foundation repair"), ("water-damage", "Water damage restoration"), ("mold", "Mold remediation"), ("waterproofing", "Basement waterproofing"), ("pest-control", "Pest & termite control")]),
  ("Yard & moving", [("decks", "Decks & patios"), ("fencing", "Fencing"), ("tree-service", "Tree service"), ("landscaping", "Landscaping & lawn"), ("moving", "Moving"), ("home-inspection", "Home inspection")]),
]
POPULAR_SERVICES = [("roofing", "Roofing"), ("hvac", "HVAC"), ("plumbing", "Plumbing"), ("remodeling", "Remodeling"), ("windows", "Windows"), ("electrical", "Electrical"), ("foundation", "Foundation"), ("water-damage", "Water damage"), ("painting", "Painting"), ("flooring", "Flooring"), ("solar", "Solar"), ("handyman", "Handyman")]

MONTHS = [
  dict(name="January", short="Jan", note="Deep winter: protect pipes, watch for ice dams and keep the furnace breathing.", tasks=[
    ("Replace HVAC filters", "1-inch filters every 1–3 months; check monthly while the heat runs constantly.", "hvac"),
    ("Check for ice dams", "Icicles and water stains on top-floor ceilings point to attic air leaks.", "insulation"),
    ("Test smoke & CO alarms", "Press-test every alarm; replace any unit older than 10 years.", ""),
    ("Inspect exposed pipes", "Insulate pipes in garages, crawl spaces and exterior walls.", "plumbing"),
    ("Clean range-hood filters", "Soak metal mesh filters in hot degreasing water.", "")]),
  dict(name="February", short="Feb", note="Plan spring projects now — contractors book out by March.", tasks=[
    ("Get spring project quotes", "Roofers, painters and deck builders fill spring calendars early.", "roofing"),
    ("Check attic for moisture", "Frost on nails or damp insulation means ventilation or air-sealing problems.", "insulation"),
    ("Clean dryer vent", "Lint buildup is a leading cause of house fires.", ""),
    ("Inspect caulk in bathrooms", "Re-caulk tubs and showers before small gaps become rot.", "remodeling")]),
  dict(name="March", short="Mar", note="Thaw season: water finds every weakness.", tasks=[
    ("Walk the roof line", "From the ground, look for missing shingles and damaged flashing after winter.", "roofing"),
    ("Test the sump pump", "Pour a bucket of water in the pit and confirm it pumps out.", "waterproofing"),
    ("Check basement for seepage", "Look for damp corners and white efflorescence on walls.", "waterproofing"),
    ("Service lawn equipment", "Sharpen mower blades and change oil before the first cut.", "landscaping")]),
  dict(name="April", short="Apr", note="Spring tune-ups keep summer bills down.", tasks=[
    ("Clean gutters & downspouts", "Clear debris and extend downspouts 4–6 ft from the foundation.", "gutters"),
    ("Schedule AC tune-up", "Have coils cleaned and refrigerant checked before the first heat wave.", "hvac"),
    ("Inspect exterior paint & siding", "Note peeling or damaged areas to fix in dry weather.", "painting"),
    ("Check window and door screens", "Repair tears before bug season.", "windows"),
    ("Look for termite swarms", "Discarded wings near windows can signal an infestation.", "pest-control")]),
  dict(name="May", short="May", note="Ideal weather for exterior work.", tasks=[
    ("Pressure-wash siding & deck", "Use low pressure on wood and vinyl to avoid damage.", "decks"),
    ("Seal or stain the deck", "If water soaks in instead of beading, it's time.", "decks"),
    ("Check irrigation system", "Fix broken heads and adjust spray away from the house.", "landscaping"),
    ("Inspect the fence line", "Tighten loose boards and reset leaning posts.", "fencing")]),
  dict(name="June", short="Jun", note="Summer storms: be ready.", tasks=[
    ("Trim trees near the house", "Keep branches at least 6–10 ft from the roof and lines.", "tree-service"),
    ("Clean the AC condenser", "Clear leaves and keep 2 ft of clearance around the unit.", "hvac"),
    ("Test GFCI outlets", "Press test and reset on kitchen, bath and outdoor outlets.", "electrical"),
    ("Check attic ventilation", "Blocked soffit vents cook shingles from below.", "roofing")]),
  dict(name="July", short="Jul", note="Peak heat: protect efficiency and safety.", tasks=[
    ("Replace HVAC filter again", "Heavy cooling loads clog filters faster.", "hvac"),
    ("Inspect for pests", "Look for ant trails, wasp nests and gnawed vents.", "pest-control"),
    ("Clean refrigerator coils", "Dusty coils make the compressor work harder.", ""),
    ("Check hose bibs for leaks", "Leaky outdoor faucets waste thousands of gallons.", "plumbing")]),
  dict(name="August", short="Aug", note="Last call for big exterior projects before fall.", tasks=[
    ("Get quotes for fall roofing or siding", "Fall is the best season for roofing and painting.", "roofing"),
    ("Flush the water heater", "Draining a few gallons removes sediment and extends life.", "plumbing"),
    ("Inspect driveway & walkways", "Seal small cracks before freeze-thaw season.", "concrete"),
    ("Review home insurance", "Confirm coverage limits reflect current rebuild costs.", "")]),
  dict(name="September", short="Sep", note="Fall prep: seal the envelope before the cold.", tasks=[
    ("Schedule furnace tune-up", "Beat the fall rush and confirm your CO safety.", "hvac"),
    ("Seal gaps around windows & doors", "Fresh caulk and weatherstripping cut drafts.", "windows"),
    ("Clean chimney & check damper", "Have wood-burning chimneys swept annually.", ""),
    ("Aerate & overseed the lawn", "Cool-season grasses thrive with fall seeding.", "landscaping")]),
  dict(name="October", short="Oct", note="Winterize before the first hard freeze.", tasks=[
    ("Clean gutters after leaf drop", "Clogged gutters cause ice dams and fascia rot.", "gutters"),
    ("Shut off & drain outdoor faucets", "Disconnect hoses and use the interior shutoff.", "plumbing"),
    ("Check attic insulation depth", "Most homes need 14–18 inches of loose fill.", "insulation"),
    ("Test the generator", "Run it under load and stock fresh fuel.", "electrical"),
    ("Store patio furniture", "Cover or store cushions and grills.", "")]),
  dict(name="November", short="Nov", note="Holiday-ready and storm-ready.", tasks=[
    ("Replace HVAC filter", "Start the heating season with a clean filter.", "hvac"),
    ("Inspect roof before snow", "Fix loose shingles and flashing now.", "roofing"),
    ("Check holiday-light circuits", "Avoid overloading outlets and use outdoor-rated cords.", "electrical"),
    ("Reverse ceiling fans", "Clockwise at low speed pushes warm air down.", ""),
    ("Stock winter supplies", "Ice melt, shovels and batteries before the first storm.", "")]),
  dict(name="December", short="Dec", note="Plan next year and protect against freezes.", tasks=[
    ("Keep pipes from freezing", "Open sink cabinets on exterior walls during cold snaps.", "plumbing"),
    ("Watch for condensation", "Persistent window condensation means humidity is too high.", "mold"),
    ("Test smoke & CO alarms", "Twice a year, every year.", ""),
    ("Set next year's project budget", "Use our cost guides to price your list.", "remodeling")]),
]

CONTEST_THEMES = ["Winter-Ready Home", "Small Space, Big Fix", "Spring Curb Appeal", "Best Budget Bathroom", "Outdoor Living Upgrade", "Kitchen on a Budget",
                  "Energy-Saver Upgrade", "Garage & Storage Glow-Up", "Back-to-School Home Office", "Fall Exterior Refresh", "DIY Repair of the Month", "Holiday-Ready Home"]
CONTEST_PRIZES = [("Grand prize", "US$250 home-improvement gift card + featured story on Home.Direct"), ("Runner-up (2)", "US$50 home-improvement gift card each"), ("Community pick", "Featured on our homepage and newsletter")]

ROI_PROJECTS = [
  ("Garage door replacement", 2000, 95), ("Steel entry door replacement", 2400, 100), ("Minor kitchen remodel (midrange)", 28000, 85),
  ("Major kitchen remodel (midrange)", 80000, 48), ("Midrange bathroom remodel", 25000, 70), ("Wood deck addition", 18000, 85),
  ("Vinyl siding replacement", 18000, 80), ("Fiber-cement siding replacement", 22000, 85), ("Vinyl window replacement", 20000, 67),
  ("Asphalt roof replacement", 30000, 57), ("Basement finishing", 35000, 70), ("Attic insulation (blown-in)", 2400, 90),
  ("Hardwood floor refinishing", 4000, 100), ("Interior repaint (whole home)", 5000, 90), ("Landscaping refresh", 6000, 85),
]

ROLES = [
  ("writer", "Freelance home-improvement writer", "Write and update cost guides and how-tos. Paid per assignment."),
  ("contractor-reviewer", "Licensed contractor reviewer", "Fact-check guides in your trade (roofing, HVAC, plumbing, electrical, remodeling). Paid per review."),
  ("video", "Short-form video creator", "Produce 30–90 second how-to and cost-explainer videos for YouTube Shorts, Reels and TikTok."),
  ("partnerships", "Local partnerships rep", "Recruit vetted local pros and sponsors in your metro. Commission-based."),
  ("community", "Community & contest moderator", "Review contest entries, moderate submissions and help judge monthly winners."),
  ("seo", "SEO & content strategist", "Plan topics, internal links and programmatic local pages."),
]
