from langchain_core.prompts import PromptTemplate

resume_txt = """
Worachot Chanmueang

CONTACT
Phone: 080-0567375
Email: mix.worachot@gmail.com
Line: mwc002
Address: Chantharakasem Subdistrict, Chatuchak District, Bangkok 10900
Linkedin: https://www.linkedin.com/in/mixworachot/

PROFESSIONAL EXPERINCE

Al Agent Developer / Product Engineer
@Avalant Co., Ltd. (JUNE 2025 - PRESENT)
Use Python, GO, Docker, K8s, Grafana, RabbitMQ and Postman.
Use no-code/low-code platforms to design and implement intelligent Al agents.
Gather customer requirements, adjust estimated times, and prepare a PoC (Proof of Concept) for the customer.

Al Application Developer (Contract)
@Amity Solutions Co., Ltd (FEB 2025 - MAR 2025)
• Enhanced chatbot response accuracy through fine-tuning and prompt engineering.
• Led comprehensive experiments and data analysis, resulting in a deployable chatbot solution.
• Adapted web chat Ul to align with customer requirements and improve user experience.
• Create Testcase chatbot response accuracy by Selenium IDE To deliver results in each Sprint.

Al Application Developer (Intern)
@Amity Solutions Co., Ltd (OCT 2024 - FEB 2025)

PROJECT EXPERIENCE

@Avalant Co.,Ltd.
AppX, PromptX, Automation workflow (https://promptxai.com/zero/login)
• We are developing an AppX that uses an agent to generate web designs based on prompts.
• Partnered with Sales/Product to capture requirements and map solutions in PromptX.ai.
• Ran demos, workshops, and POCs (Q&A, booking, complaint triage) built 100% no-code.
• Turned business needs into automation flows: triggers, routing, approvals, notifications, guardrails.
• Wrote proposals, high-level diagrams, and functional specs..
• Advised on integrations via PromptX connectors (APIs, webhooks, LINE, email) and deployment options.
• Fed client feedback to Product and tracked Al/automation trends to update templates and roadmap.

@Amity Solutions Co., Ltd
EGAT SMART LIFE (กฟผ.), APOLLO, KCMH AI KIOSK
• Enhanced chatbot accuracy through fine-tuning and prompt design; delivered a deployable solution, customized Ul for user needs, led weekly updates and knowledge sharing, Create Testcase chatbot response accuracy by Selenium IDE

@Unversity of Phayao
Developing a Chatbot in Line OA with Gemini to answer questions for students
• Utilized VertexAl and Gemini model for development and training data preparation.
Managed the entire project lifecycle, from planning to deployment, ensuring timely delivery and high-quality results.

EDUCATION
@University of Phayao | 2021-2024
• Bachrlor degree computer engineering

SKILLS
• JavaScript
• Python
• GO
• Agile/Scrum
• Wireframe.
• Architecture Diagram

TOOLS
• Github
• Automation workflow (e.g. n8n, PromptX)
• Docker
• Grafana
• Postman

SOFT SKILLS
• Speaking
• Presentation
• Coordinate
• Demonstrate
• Productrainer
 """

SYSTEM_PROMPT = PromptTemplate.from_template("""
You are a personal assistant for Worachot Chanmueang his name is "Mix". You will help recruiters to
understand his resume and answer any questions they have about his skills, experience, and qualifications.
This is his resume: {resume_text}.
"""
)