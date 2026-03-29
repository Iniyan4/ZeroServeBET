ZeroServe - "Smart Food Rescue and Redistribution Platform” 
A scalable platform for intelligent food redistribution and waste reduction. 
Impact 
“Feed people, not landfills.” 
Overview 
ZeroServe is a full-stack platform designed to reduce food wastage by efficiently connecting 
donors, NGOs, delivery partners, and administrators. The system ensures that surplus food 
is redistributed quickly, safely, and transparently using structured workflows and intelligent 
prioritization. 
Problem Statement 
FoodBridge: Real-Time Surplus Food Redistribution Platform A significant 
amount of food waste occurs at the consumer level due to the absence of efficient 
redistribution systems. Surplus food often goes unused because there is no real-time 
mechanism to connect individuals or providers with those who need it. Additionally, limited 
awareness and poor coordination further hinder timely redistribution. This gap leads to 
increased food wastage, contributing to environmental damage and lost opportunities to 
combat hunger. Without a reliable and trusted system to manage logistics, safety, and 
accessibility, surplus food cannot be effectively utilized to support communities in need. 
Solution 
ZeroServe provides an integrated ecosystem that enables seamless food redistribution 
through: 
● Structured multi-role interaction (Donor, NGO, Delivery Partner, Admin) 
● Smart prioritization based on expiry and urgency 
● End-to-end tracking of food lifecycle 
● Reliability monitoring and administrative control 
● AI-assisted insights for decision support 
System Architecture 
The system was developed using a structured two-layer approach: 
● Frontend: UI, dashboards, routing, and data mapping 
● Backend: APIs, database models, business logic, and intelligence layer 
Both layers were synchronized using a predefined API contract and integrated incrementally 
Tech Stack 
Frontend 
● React.js 
● Vite 
● Tailwind CSS 
● Framer Motion 
● React Router 
● Axios 
Backend 
● Django / Node.js 
● REST API architecture 
● JWT Authentication 
Database 
● MySQL 
Intelligence Layer 
● LLM-based analysis for risk evaluation and administrative insights 
Implementation Approach 
The system was developed using a layered and modular architecture with parallel 
development. 
Frontend 
● Built responsive dashboards for all user roles 
● Developed reusable UI components such as cards, forms, timelines, and analytics 
panels 
● Implemented routing and role-based navigation 
● Integrated APIs using a consistent request/response structure 
Backend 
● Designed relational database schema with clear entity relationships 
● Implemented REST APIs for all modules 
● Developed core business logic including: 
○ Food lifecycle management 
○ Claim handling 
○ Delivery coordination 
○ Reliability scoring 
● Integrated authentication using JWT 
Integration Strategy 
● Defined API contracts before development 
● Used mock data for frontend development initially 
● Integrated modules incrementally (authentication, listings, delivery, admin) 
Features 
Multi-Role System 
● Donor 
● NGO 
● Delivery Partner 
● Administrator 
Food Listing and Management 
● Create and manage food listings 
● Expiry tracking and urgency scoring 
● Status-based lifecycle management 
NGO Discovery and Claiming 
● Browse nearby and recommended listings 
● Claim and manage food requests 
Delivery Management 
● Task assignment and tracking 
● Status updates (pickup, transit, delivery) 
● Timeline visualization 
Reliability and Monitoring 
● Track user behavior and interactions 
● Flag suspicious activities 
● Restrict unreliable users 
Notifications System 
● Updates for listing status, claims, and delivery 
Analytics Dashboard 
● Donation statistics 
● Operational performance insights 
● Platform usage metrics 
Innovation 
ZeroServe introduces several key innovations compared to traditional donation systems: 
● Urgency-based prioritization that automatically ranks food listings based on 
estimated expiry time to ensure perishable food is distributed first 
● End-to-end workflow integration connecting donors, NGOs, delivery partners, and 
administrators in a single coordinated system from listing to delivery 
● Reliability scoring mechanism that evaluates user behavior across all roles to ensure 
accountability and reduce misuse 
● AI-assisted administrative insights that provide intelligent reports on system activity, 
helping administrators identify risks and make informed decisions 
● Modular architecture that supports scalability and allows seamless integration of new 
features such as analytics, AI models, and multi-region expansion 
● Comprehensive admin monitoring system that tracks individual customer 
performance, including total food received, NGOs serving them, delivery partners 
involved, and customer feedback 
● Donor and restaurant analytics that provide daily summaries of food distributed, list of 
customers served, and quantity of food delivered 
● Delivery partner performance tracking that records number of deliveries completed 
and associated customers served 
● AI-generated reports for customers, donors, and delivery partners that highlight 
performance trends, suspicious behavior, and reliability concerns, enabling admins to 
take appropriate actions 
● Food quality assurance through an expiry estimation mechanism that calculates 
freshness based on preparation time and food type, ensuring safe and efficient 
redistribution 
Future Enhancements 
● Real-time map-based tracking 
● Push notification system 
● Mobile application 
● Advanced predictive analytics for demand forecasting 
● Multi-city and large-scale deployment 
● Blockchain-based transparency for donations 
● Enhanced AI-driven recommendation systems 
Bugs remaining  
● Partial backend integration for certain modules 
● Some pages rely on placeholder or mock data 
● Delivery tracking not fully real-time 
● Notifications system not fully implemented 
● Minor UI responsiveness improvements required 
Conclusion 
ZeroServe provides a scalable and intelligent approach to food redistribution by combining 
structured workflows, real-time coordination, and data-driven decision-making. The platform 
has the potential to significantly reduce food wastage and improve accessibility to surplus 
resources. 

# Live Frontend
 https://github.com/Iniyan4/ZeroServeFE.git

# Demo Link
 https://drive.google.com/file/d/1050B1SUvZ9E0JvOR73cp94ZGcaOmkUML/view?usp=sharing
