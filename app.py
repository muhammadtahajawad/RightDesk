import gradio as gr
import requests
import os

API_KEY = os.environ.get("GROQ_API_KEY")

SYSTEM_PROMPT = """You are RightDesk, an AI legal ACTION assistant for Pakistan.

Your purpose is NOT to explain law.
Your purpose is to convert real-life problems into CLEAR ACTION and READY-TO-USE LEGAL DOCUMENTS.

Always respond EXACTLY in this structured format:

🔍 SITUATION SUMMARY
Explain the user's situation in 2-3 simple, clear sentences.

⚖️ YOUR LEGAL RIGHTS
List 3-4 practical rights the user has under Pakistani law.
Keep them direct and easy to understand.

📋 IMMEDIATE ACTION STEPS (DO THIS NOW)
Step 1: ...
Step 2: ...
Step 3: ...
Make steps realistic and actionable.

📝 READY-TO-SUBMIT COMPLAINT / FIR
Write a clean, properly formatted legal document that the user can directly copy and submit.

Format it like this and add the hypen's line before starting and ending of it as shown:

--------------------------------
To: Station House Officer (SHO)
[Police Station Name]

Subject: Complaint regarding [brief issue]

I, [FULL NAME], CNIC [XXXXX-XXXXXXX-X], resident of [ADDRESS], hereby report that:

[Clear description of incident in formal tone]

I request you to kindly take legal action under relevant laws and register my complaint/FIR at the earliest.

Date: [DATE]
Signature: __________
Contact: [PHONE NUMBER]
--------------------------------

IMPORTANT:
- Make it look real and official
- Use simple but formal language
- No placeholders like "..." inside body

🏛️ WHERE TO GO / REPORT
Clearly tell the user:
- Exact authority (Police, FIA, Labor Court, NADRA, etc.)
- What to say when they go
- Any escalation option (e.g., SP, helpline)

RULES:
- No legal jargon
- No long explanations
- Focus on ACTION, not theory
- Make the user feel confident and guided

User problem:
"""


def get_legal_help(user_problem):
    if not user_problem.strip():
        return "⚠️ Please describe your problem first. / براہ کرم پہلے اپنا مسئلہ بیان کریں۔"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_problem}
        ]
    }
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers=headers,
        json=data
    )
    result = response.json()
    if "choices" in result:
        return result["choices"][0]["message"]["content"]
    else:
        return f"API Error: {str(result)}"


def clear_input():
    return "", ""


def load_example(example_text):
    return example_text


custom_css = """
@font-face {
    font-family: 'jameel-noori-nastaleeq';
    src: url('https://cdn.jsdelivr.net/gh/tariq-abdullah/urdu-web-font-CDN/JameelNooriNastaleeq.woff') format('woff');
}
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500&display=swap');
* { box-sizing: border-box; }
body, .gradio-container {
    background-color: #0a0a0f !important;
    color: #e8e0d0 !important;
}
.gradio-container {
    max-width: 900px !important;
    margin: 0 auto !important;
    font-family: 'Inter', sans-serif !important;
}
#header {
    text-align: center;
    padding: 44px 20px 16px 20px;
    border-bottom: 1px solid #c8a951;
    margin-bottom: 28px;
}
#header h1 {
    font-family: 'Playfair Display', serif !important;
    font-size: 2.8em !important;
    color: #c8a951 !important;
    margin-bottom: 6px !important;
    letter-spacing: 2px;
}
#header .subtitle-en {
    color: #aaa !important;
    font-size: 0.9em !important;
    font-style: italic;
    margin-bottom: 4px;
}
#header .subtitle-ur {
    font-family: 'jameel-noori-nastaleeq', serif !important;
    color: #c8a951 !important;
    font-size: 1.4em !important;
    direction: rtl;
    line-height: 2;
}
#disclaimer {
    background-color: #1a1400;
    border-left: 4px solid #c8a951;
    padding: 12px 16px;
    border-radius: 4px;
    margin-bottom: 24px;
    font-size: 0.83em;
    color: #c8a951;
}
#disclaimer .ur {
    font-family: 'jameel-noori-nastaleeq', serif !important;
    direction: rtl;
    display: block;
    font-size: 1.3em;
    margin-top: 6px;
    line-height: 2;
}
/* CHANGE 1 — slightly larger examples label */
#examples-label {
    color: #aaa;
    font-size: 0.95em;
    margin-bottom: 8px;
    margin-top: 4px;
}
.example-btn {
    background-color: #1a1a2e !important;
    color: #c8a951 !important;
    border: 1px solid #c8a951 !important;
    border-radius: 4px !important;
    font-size: 0.8em !important;
    padding: 6px 12px !important;
    cursor: pointer !important;
    margin: 4px !important;
    font-family: 'Inter', sans-serif !important;
}
.example-btn:hover {
    background-color: #c8a951 !important;
    color: #0a0a0f !important;
}
textarea, .gr-textbox textarea {
    background-color: #111120 !important;
    color: #e8e0d0 !important;
    border: 1px solid #333355 !important;
    border-radius: 6px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95em !important;
}
textarea:focus {
    border-color: #c8a951 !important;
    outline: none !important;
}
/* CHANGE 2 — Urdu part of label in Jameel Noori */
label .ur-label, .gr-textbox label .ur-label {
    font-family: 'jameel-noori-nastaleeq', serif !important;
    font-size: 1.25em !important;
    direction: rtl;
    display: inline-block;
    margin-right: 4px;
}
label, .gr-textbox label {
    color: #c8a951 !important;
    font-weight: 500 !important;
}
/* CHANGE 3 — Urdu part of buttons in Jameel Noori */
.gr-button {
    font-family: 'Inter', sans-serif !important;
    border-radius: 4px !important;
    font-size: 0.95em !important;
    padding: 11px 22px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
}
.gr-button-primary {
    background-color: #c8a951 !important;
    color: #0a0a0f !important;
    border: none !important;
    font-weight: 600 !important;
}
.gr-button-primary:hover {
    background-color: #e0c060 !important;
}
.gr-button-secondary {
    background-color: transparent !important;
    color: #c8a951 !important;
    border: 1px solid #c8a951 !important;
}
.gr-button-secondary:hover {
    background-color: #1a1400 !important;
}
#output_box, .gr-markdown {
    background-color: #111120 !important;
    border: 1px solid #333355 !important;
    border-radius: 6px !important;
    padding: 24px !important;
    color: #e8e0d0 !important;
    font-size: 0.95em !important;
    line-height: 1.9 !important;
    min-height: 80px;
}
#output_box p, #output_box li {
    color: #e8e0d0 !important;
}
#output_box strong {
    color: #c8a951 !important;
}
#footer {
    text-align: center;
    padding: 20px;
    font-size: 0.76em;
    color: #555;
    border-top: 1px solid #1e1e2e;
    margin-top: 30px;
}
#footer .ur {
    font-family: 'jameel-noori-nastaleeq', serif !important;
    direction: rtl;
    display: block;
    font-size: 2em;
    margin-top: 6px;
    color: #666;
    line-height: 2;
}
#badge {
    display: inline-block;
    background-color: #1a1a2e;
    border: 1px solid #c8a951;
    color: #c8a951;
    font-size: 0.75em;
    padding: 3px 10px;
    border-radius: 20px;
    margin-top: 8px;
    letter-spacing: 0.5px;
}
"""

EXAMPLES = [
    "🏠 Landlord Eviction -- My landlord kicked me out without notice and kept my deposit of 50,000 rupees.",
    "💼 Salary Theft -- My employer hasn't paid my salary for 3 months and is threatening to fire me.",
    "👩 Harassment -- I am being harassed by my neighbor. He threatens me daily and I am scared.",
    "🏦 Bank Fraud -- Someone used my CNIC to take a loan from a bank without my knowledge.",
]

with gr.Blocks(css=custom_css, title="RightDesk — AI Legal Assistant Pakistan") as app:

    gr.HTML("""
    <div id="header">
        <h1>⚖️ RightDesk</h1>
        <p class="subtitle-en">AI Legal Action Assistant for Pakistan</p>
        <p class="subtitle-ur">پاکستان کے لیے مصنوعی ذہانت پر مبنی قانونی مددگار</p>
        <span id="badge">🌐 SDG 16 -- Peace, Justice & Strong Institutions</span>
    </div>
    """)

    gr.HTML("""
    <div id="disclaimer">
        ⚠️ <strong>Disclaimer:</strong> RightDesk provides general legal guidance only. For serious matters, consult a qualified lawyer.
        <span class="ur">یہ ٹول صرف عمومی قانونی رہنمائی فراہم کرتا ہے۔ سنگین معاملات میں کسی وکیل سے رجوع کریں۔</span>
    </div>
    """)

    gr.HTML('<p id="examples-label">💡 Quick Examples -- Click to Load:</p>')

    with gr.Row():
        ex1 = gr.Button(EXAMPLES[0], elem_classes="example-btn")
        ex2 = gr.Button(EXAMPLES[1], elem_classes="example-btn")

    with gr.Row():
        ex3 = gr.Button(EXAMPLES[2], elem_classes="example-btn")
        ex4 = gr.Button(EXAMPLES[3], elem_classes="example-btn")

    problem_input = gr.Textbox(
        label="Describe Your Problem / اپنا مسئلہ بیان کریں",
        placeholder="Type your legal problem in English or Urdu...",
        lines=5
    )

    with gr.Row():
        submit_btn = gr.Button("⚖️ Get Legal Help / قانونی مدد حاصل کریں", variant="primary")
        clear_btn = gr.Button("🗑️ Clear / صاف کریں", variant="secondary")

    output = gr.Markdown(
        label="Your Legal Action Plan / آپ کا قانونی لائحہ عمل",
        elem_id="output_box"
    )

    submit_btn.click(fn=get_legal_help, inputs=problem_input, outputs=output)
    clear_btn.click(fn=clear_input, inputs=[], outputs=[problem_input, output])

    ex1.click(fn=lambda: EXAMPLES[0], inputs=[], outputs=problem_input)
    ex2.click(fn=lambda: EXAMPLES[1], inputs=[], outputs=problem_input)
    ex3.click(fn=lambda: EXAMPLES[2], inputs=[], outputs=problem_input)
    ex4.click(fn=lambda: EXAMPLES[3], inputs=[], outputs=problem_input)

    gr.HTML("""
    <div id="footer">
        RightDesk &copy; 2026 &nbsp;|&nbsp; Muhammad Taha Jawad | Sana Akbar | Wasif Abdul Qayyum | Summaiyah Maqsood | Syed Obaid | Muhammad Danish
        <br>
        Built for SDG 16: Peace, Justice &amp; Strong Institutions 
        <br>
        <span id="badge" style="font-family: 'jameel-noori-nastaleeq', serif; font-size: 1.6em; direction: rtl; margin-top: 8px; display: inline-block;">امن، انصاف اور مضبوط ادارے</span>
    </div>
    """)

app.launch()