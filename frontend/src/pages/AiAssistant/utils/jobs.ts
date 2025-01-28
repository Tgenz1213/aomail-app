interface Profile {
    title: string;
    description: string;
    keywords: string[];
    important: string;
    informative: string;
    useless: string;
}

export const predefinedProfiles: Profile[] = [
    {
        title: "Software Engineer",
        description: "Developer working on software projects and technical systems",
        keywords: ["programming", "development", "tech", "coding", "software", "engineering"],
        important:
            "Critical production issues, urgent pull request reviews, deployment coordination messages, and direct messages from team leads about blocking issues. Example: 'Production database is down' or 'Urgent security patch needed'.",
        informative:
            "Code review requests, sprint planning updates, technical documentation changes, and non-urgent bug reports. Example: 'New feature documentation added' or 'Weekly sprint report'.",
        useless:
            "Marketing emails about development tools, automated CI/CD success notifications, and promotional content about tech conferences. Example: 'Try our new IDE' or 'Build passed successfully'.",
    },
    {
        title: "IT Support",
        description: "Technical support and system administration",
        keywords: ["IT", "support", "helpdesk", "technical", "systems", "administration"],
        important:
            "Critical system alerts, urgent tickets, system outages, security incidents. Example: 'Production system down' or 'Security breach detected'.",
        informative:
            "Regular maintenance notifications, system updates, ticket status changes. Example: 'Scheduled maintenance window' or 'Ticket resolution summary'.",
        useless:
            "Security awareness newsletters, vendor promotions, general IT news. Example: 'New security training available' or 'IT vendor showcase'.",
    },
    {
        title: "Teacher/Professor",
        description: "Educational professional in K-12 or higher education",
        keywords: ["education", "teaching", "academic", "instructor", "faculty", "professor"],
        important:
            "Student emergencies, parent conferences, grade submission deadlines, department head directives, classroom incidents requiring immediate attention. Example: 'Student medical emergency during class' or 'Urgent parent meeting request regarding student behavior'.",
        informative:
            "Lesson plan submissions, faculty meeting notes, curriculum updates, student progress reports, workshop announcements. Example: 'Next week's department meeting agenda' or 'Quarterly grade submission reminder'.",
        useless:
            "Educational product marketing, general school newsletters not affecting your classes, third-party workshop advertisements. Example: 'Buy our new textbook series' or 'General campus events newsletter'.",
    },
    {
        title: "Student",
        description: "University, college, or continuing education learner",
        keywords: ["student", "education", "university", "college", "academic", "learning"],
        important:
            "Professor communications, assignment deadlines, exam schedules, registration deadlines. Example: 'Final exam room change' or 'Course registration deadline today'.",
        informative:
            "Course materials, study group updates, campus announcements, academic resources. Example: 'Study group meeting time' or 'New course materials posted'.",
        useless:
            "Campus event promotions, submission confirmations, marketing emails. Example: 'Campus store sale' or 'Join student club newsletter'.",
    },
    {
        title: "Nurse",
        description: "Healthcare professional providing patient care",
        keywords: ["nursing", "healthcare", "patient care", "medical", "clinical", "health"],
        important:
            "Patient emergencies, critical lab results, medication errors, shift emergency coverage, immediate care requirements. Example: 'Code Blue in Ward 3' or 'Critical lab values for patient in Room 204'.",
        informative:
            "Shift handover notes, routine patient updates, scheduled training sessions, policy updates. Example: 'Updated infection control protocols' or 'Monthly staff rotation schedule'.",
        useless:
            "Medical equipment marketing, general hospital newsletters, non-mandatory conference invitations. Example: 'New scrubs catalog' or 'Hospital cafeteria menu'.",
    },
    {
        title: "Manager",
        description: "Team leadership and project management across industries",
        keywords: ["leadership", "management", "team lead", "supervisor", "director", "coordination"],
        important:
            "Urgent escalations from team members, critical client issues, budget approvals needed within 24h, and emergency stakeholder communications. Example: 'Team blocked on critical deliverable' or 'Client escalation needs immediate attention'.",
        informative:
            "Weekly team performance reports, project status updates, resource allocation requests, and non-urgent team member feedback. Example: 'Monthly department metrics' or 'Team capacity planning'.",
        useless:
            "General company newsletters, office maintenance notifications, and non-relevant department updates. Example: 'Office plant watering schedule' or 'Cafeteria menu updates'.",
    },
    {
        title: "Sales Representative",
        description: "B2B or B2C sales and business development",
        keywords: ["sales", "business development", "account management", "client relations", "deals"],
        important:
            "Client inquiries, deal updates, urgent prospect requests, sales target alerts. Example: 'Hot lead requires immediate follow-up' or 'Client contract pending urgent approval'.",
        informative:
            "Market reports, competitor updates, pipeline status, sales metrics. Example: 'Weekly sales dashboard' or 'New competitor analysis'.",
        useless:
            "Internal newsletters, system notifications, non-relevant product updates. Example: 'Office social event' or 'Generic industry newsletter'.",
    },
    {
        title: "Lawyer",
        description: "Legal practice and case management",
        keywords: ["legal", "law", "attorney", "counsel", "litigation", "judicial"],
        important:
            "Court deadlines, client emergencies, filing deadlines, urgent case updates. Example: 'Court filing due today' or 'Emergency client situation'.",
        informative:
            "Legal updates, case law changes, client meeting schedules, document reviews. Example: 'New precedent case published' or 'Client meeting notes'.",
        useless:
            "Legal vendor marketing, networking events, general newsletters. Example: 'Law firm social event' or 'Legal software promotion'.",
    },
    {
        title: "Creative Professional",
        description: "Designer, writer, artist, or content creator",
        keywords: ["creative", "design", "art", "content", "writing", "media"],
        important:
            "Client feedback, project deadlines, revision requests, urgent approvals. Example: 'Final artwork approval needed' or 'Emergency content update required'.",
        informative:
            "Design resources, creative briefs, project updates, style guides. Example: 'Brand guidelines updated' or 'New project brief'.",
        useless:
            "Design tool promotions, industry newsletters, non-relevant training ads. Example: 'Try new design software' or 'Creative conference early bird'.",
    },
    {
        title: "Restaurant Staff",
        description: "Restaurant workers including servers, cooks, and managers",
        keywords: ["restaurant", "food service", "kitchen", "hospitality", "culinary", "server"],
        important:
            "Food safety alerts, equipment breakdowns, staff no-shows, large party reservations requiring immediate attention. Example: 'Refrigeration system failure' or 'Emergency health inspector visit'.",
        informative:
            "Menu changes, shift schedules, inventory counts, supplier updates. Example: 'Weekly ingredient delivery schedule' or 'New menu item training'.",
        useless:
            "Restaurant equipment marketing, general food industry newsletters, non-relevant vendor catalogs. Example: 'Subscribe to cooking magazine' or 'Random supplier promotional menu'.",
    },
    {
        title: "Beauty Professional",
        description: "Hairstylist, beautician, or salon owner",
        keywords: ["salon", "beauty", "styling", "cosmetics", "aesthetics", "spa"],
        important:
            "Client emergencies, supply shortages affecting appointments, equipment failures, scheduling conflicts. Example: 'Water outage affecting today's appointments' or 'Emergency client rescheduling needed'.",
        informative:
            "Appointment confirmations, product inventory updates, client feedback, style trend updates. Example: 'Next week's booking schedule' or 'New product training available'.",
        useless:
            "Generic beauty product marketing, non-relevant industry news, spam promotions. Example: 'General beauty industry newsletter' or 'Random product catalogs'.",
    },
    {
        title: "Small Business Owner",
        description: "Independent retail or service business operator",
        keywords: ["retail", "small business", "entrepreneur", "shop owner", "merchant", "proprietor"],
        important:
            "Supplier delivery issues, POS system failures, security incidents, urgent staff matters. Example: 'Store security alarm triggered' or 'Emergency product recall notice'.",
        informative:
            "Sales reports, inventory levels, employee schedules, vendor updates. Example: 'Weekly sales summary' or 'Upcoming holiday inventory planning'.",
        useless:
            "Unsolicited vendor pitches, general retail industry newsletters, random marketing materials. Example: 'Subscribe to retail magazine' or 'Random vendor catalog'.",
    },
    {
        title: "Freelance Professional",
        description: "Independent contractor or freelance worker",
        keywords: ["freelance", "contractor", "independent", "self-employed", "gig", "consultant"],
        important:
            "Client project deadlines, contract negotiations, payment issues, urgent revision requests. Example: 'Final deliverable needed by EOD' or 'Urgent client feedback requiring immediate attention'.",
        informative:
            "Project updates, potential client inquiries, industry opportunities, networking events. Example: 'Project milestone review' or 'Potential client introduction'.",
        useless:
            "Platform marketing emails, general freelance newsletters, non-relevant job postings. Example: 'Try our premium freelance tools' or 'Generic networking event invitation'.",
    },
    {
        title: "Field Technician",
        description: "On-site technical support and maintenance professional",
        keywords: ["technician", "maintenance", "repair", "field service", "installation", "support"],
        important:
            "Emergency repair calls, safety incidents, critical equipment failures, immediate service requests. Example: 'Emergency generator failure at Hospital' or 'Critical system down requiring immediate attention'.",
        informative:
            "Maintenance schedules, equipment updates, training materials, service logs. Example: 'Next week's maintenance schedule' or 'New equipment installation guidelines'.",
        useless:
            "Tool vendor marketing, general industry newsletters, non-relevant training offers. Example: 'Subscribe to tech magazine' or 'Random tool catalog'.",
    },
    {
        title: "Research Scientist",
        description: "Academic or industrial researcher",
        keywords: ["research", "science", "laboratory", "investigation", "academic", "scientific"],
        important:
            "Lab safety incidents, grant deadlines, critical experiment issues, immediate funding matters. Example: 'Lab safety breach requires immediate action' or 'Grant submission deadline today'.",
        informative:
            "Research findings, collaboration opportunities, conference deadlines, publication updates. Example: 'Latest experiment results' or 'Upcoming conference abstract deadline'.",
        useless:
            "Lab equipment marketing, general science newsletters, non-relevant conference spam. Example: 'New microscope catalog' or 'Random research magazine subscription'.",
    },
    {
        title: "Construction Worker",
        description: "Construction and building trades professional",
        keywords: ["construction", "building", "trades", "contractor", "site work", "labor"],
        important:
            "Safety violations, weather impacts on projects, urgent material shortages, equipment failures. Example: 'Site safety violation needs immediate action' or 'Critical equipment malfunction on site'.",
        informative:
            "Project timelines, material deliveries, inspection schedules, site access updates. Example: 'Tomorrow's concrete delivery schedule' or 'Updated site safety protocols'.",
        useless:
            "Construction equipment marketing, general industry newsletters, non-relevant training ads. Example: 'New tool catalog' or 'General construction magazine'.",
    },
    {
        title: "Driver/Delivery Professional",
        description: "Transportation and delivery service professional",
        keywords: ["driver", "delivery", "transport", "logistics", "shipping", "courier"],
        important:
            "Route changes, vehicle issues, delivery emergencies, traffic incidents. Example: 'Vehicle breakdown requiring immediate assistance' or 'Urgent route change due to road closure'.",
        informative:
            "Schedule updates, maintenance reminders, route planning, fuel logs. Example: 'Next week's delivery schedule' or 'Vehicle maintenance due notice'.",
        useless:
            "Vehicle sales marketing, general transport newsletters, non-relevant insurance ads. Example: 'Buy new trucks' or 'Random logistics magazine'.",
    },
    {
        title: "Administrative Professional",
        description: "Office administration and support professional",
        keywords: ["admin", "office", "clerical", "secretary", "coordinator", "assistant"],
        important:
            "Executive calendar conflicts, urgent meeting changes, critical document deadlines, office emergencies. Example: 'CEO schedule conflict needs immediate resolution' or 'Urgent board meeting document required'.",
        informative:
            "Office supplies inventory, meeting schedules, filing systems, procedure updates. Example: 'Monthly calendar update' or 'New filing system guidelines'.",
        useless:
            "Office supply marketing, general admin newsletters, non-relevant software ads. Example: 'New printer catalog' or 'Random office magazine'.",
    },
    {
        title: "Financial Professional",
        description: "Financial and accounting professional",
        keywords: ["finance", "accounting", "banking", "investment", "bookkeeping", "tax"],
        important:
            "Tax deadlines, audit notices, client financial emergencies, reporting errors. Example: 'Critical tax filing deadline today' or 'Urgent audit document request'.",
        informative:
            "Financial reports, client updates, regulatory changes, software updates. Example: 'Monthly reconciliation reminder' or 'New tax regulation update'.",
        useless:
            "Financial software marketing, general accounting newsletters, non-relevant training ads. Example: 'Try new accounting software' or 'Random finance magazine'.",
    },
];
