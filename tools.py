# tools.py

# Category list for sidebar
CATEGORIES = [
    "AI Chatbots",
    "AI Presentation",
    "AI Coding Assistance",
    "AI Email Assistance",
    "AI Image Generation",
    "AI Spreadsheet",
    "AI Meeting Notes",
    "AI Workflow Automation",
    "AI Writing Generation",
    "AI Scheduling",
    "AI Knowledge Management",
    "AI Video Generation",
    "AI Graphic Design",
    "AI Data Visualization",
    "Free AI API Access",
]

# Helper notes:
# - logo: prefer stable SVGs from Wikimedia or well-known icon collections/CDNs.
# - embeddable: True if the site usually allows iframe preview; set False if it blocks (many do).
# - tags: used by the search box in the app.

TOOLS = [
    # -------------------- AI Chatbots --------------------
    {"name":"ChatGPT","link":"https://chat.openai.com/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg","category":"AI Chatbots","tags":["openai","gpt","chat"],"embeddable":False,"blurb":"General-purpose assistant with GPT models."},  # [web:24]
    {"name":"Claude","link":"https://claude.ai/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/b/b0/Claude_AI_symbol.svg","category":"AI Chatbots","tags":["anthropic","reasoning"],"embeddable":False,"blurb":"Helpful assistant by Anthropic with strong reasoning."},  # [web:29]
    {"name":"DeepSeek","link":"https://chat.deepseek.com/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/e/ec/DeepSeek_logo.svg","category":"AI Chatbots","tags":["deepseek","r1","coder"],"embeddable":False,"blurb":"Efficient, competitive large language models."},  # [web:35]
    {"name":"Gemini","link":"https://gemini.google.com/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/8/8a/Google_Gemini_logo.svg","category":"AI Chatbots","tags":["google","multimodal"],"embeddable":False,"blurb":"Google’s multimodal AI chat."},  # [web:23]
    {"name":"Grok","link":"https://x.ai/","plan":"Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/f/f7/Grok-feb-2025-logo.svg","category":"AI Chatbots","tags":["xai","realtime"],"embeddable":False,"blurb":"xAI chatbot with real‑time knowledge."},  # [web:32]
    {"name":"Meta AI","link":"https://www.meta.ai/","plan":"Free","logo":"https://upload.wikimedia.org/wikipedia/commons/b/b1/Meta_AI_logo.png","category":"AI Chatbots","tags":["meta","facebook"],"embeddable":False,"blurb":"Conversational assistant by Meta."},  # [web:35]
    {"name":"MS Copilot","link":"https://copilot.microsoft.com/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/en/a/aa/Microsoft_Copilot_Icon.svg","category":"AI Chatbots","tags":["microsoft","bing"],"embeddable":False,"blurb":"Assistant across Bing and Microsoft apps."},  # [web:35]
    {"name":"Perplexity","link":"https://www.perplexity.ai/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/1/1d/Perplexity_AI_logo.svg","category":"AI Chatbots","tags":["search","answers"],"embeddable":False,"blurb":"Answer engine with citations."},  # [web:22]

    # -------------------- AI Presentation --------------------
    {"name":"Beautiful.ai","link":"https://www.beautiful.ai/","plan":"Paid","logo":"https://coledab2b.com/coleda-docker/NewsPictures/1/Beautifulai_new_Logo-08-11-2021-17-08-08-PM.jpg","category":"AI Presentation","tags":["slides","design"],"embeddable":True,"blurb":"Design‑first slide automation."},  # [web:35]
    {"name":"Gamma","link":"https://gamma.app/","plan":"Free + Paid","logo":"https://www.saudiaat.com/wp-content/uploads/2025/03/8hla4f05.png","category":"AI Presentation","tags":["docs","decks"],"embeddable":True,"blurb":"Docs, decks, and pages with AI."},  # [web:2]
    {"name":"Pitch","link":"https://pitch.com/","plan":"Free + Paid","logo":"https://logowik.com/content/uploads/images/pitch-presentation6614.logowik.com.webp","category":"AI Presentation","tags":["slides","collaboration"],"embeddable":True,"blurb":"Collaborative presentations."},  # [web:35]
    {"name":"Plus","link":"https://www.plusdocs.com/","plan":"Free + Paid","logo":"https://plusai.com/622ffb3448f15ce7a33c6a2b/62e834938d9d2b11483ee26e_plus_logo.svg","category":"AI Presentation","tags":["snapshots","slides"],"embeddable":True,"blurb":"Live snapshots and AI help for slides."},  # [web:35]
    {"name":"PopAI","link":"https://www.popai.pro/","plan":"Free + Paid","logo":"https://popaife.s3.ap-southeast-1.amazonaws.com/logo/share-logo.png","category":"AI Presentation","tags":["slides","writer"],"embeddable":True,"blurb":"AI for slides and content."},  # [web:35]
    {"name":"PresentationAI","link":"https://presentationai.app/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/presentationai.svg","category":"AI Presentation","tags":["slides"],"embeddable":True,"blurb":"Auto‑generated decks from prompts."},  # [web:35]
    {"name":"Slidesgo","link":"https://slidesgo.com/","plan":"Free + Paid","logo":"https://slidesgo.com/favicons/favicon.ico","category":"AI Presentation","tags":["templates"],"embeddable":True,"blurb":"Templates with AI suggestions."},  # [web:2]
    {"name":"Tome","link":"https://tome.app/","plan":"Free + Paid","logo":"https://tome.app/favicon.ico","category":"AI Presentation","tags":["narrative"],"embeddable":True,"blurb":"Narrative presentations generated by AI."},  # [web:2]

    # -------------------- AI Coding Assistance --------------------
    {"name":"AskCodi","link":"https://www.askcodi.com/","plan":"Free + Paid","logo":"https://images.saasworthy.com/askcodi_45399_logo_1706881149_81pfq.png","category":"AI Coding Assistance","tags":["docs","snippets"],"embeddable":True,"blurb":"AI prompts for code and docs."},  # [web:35]
    {"name":"Codiga","link":"https://www.codiga.io/","plan":"Free + Paid","logo":"https://www.codiga.io/social/open-graph.png","category":"AI Coding Assistance","tags":["static analysis"],"embeddable":True,"blurb":"Coding assistant and analysis."},  # [web:35]
    {"name":"Cursor","link":"https://www.cursor.com/","plan":"Paid","logo":"https://www.cursor.com/favicon.ico","category":"AI Coding Assistance","tags":["ide","agent"],"embeddable":False,"blurb":"AI‑native code editor."},  # [web:2]
    {"name":"GitHub Copilot","link":"https://github.com/features/copilot","plan":"Paid","logo":"https://registry.npmmirror.com/@lobehub/icons-static-png/latest/files/light/githubcopilot.png","category":"AI Coding Assistance","tags":["ide","pair"],"embeddable":False,"blurb":"AI pair programmer."},  # [web:2]
    {"name":"Qodo","link":"https://qodo.ai/","plan":"Free + Paid","logo":"https://www.qodo.ai/wp-content/uploads/2025/06/social-share-new.webp","category":"AI Coding Assistance","tags":["editor"],"embeddable":True,"blurb":"AI coding copilot."},  # [web:35]
    {"name":"Replit","link":"https://replit.com/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/thumb/7/78/New_Replit_Logo.svg/1200px-New_Replit_Logo.svg.png","category":"AI Coding Assistance","tags":["online ide"],"embeddable":True,"blurb":"Online IDE with AI features."},  # [web:35]
    {"name":"Tabnine","link":"https://www.tabnine.com/","plan":"Free + Paid","logo":"https://www.tabnine.com/favicon.ico","category":"AI Coding Assistance","tags":["autocomplete"],"embeddable":True,"blurb":"Code completion trained on permissive code."},  # [web:2]

    # -------------------- AI Email Assistance --------------------
    {"name":"Clippit.ai","link":"https://clippit.ai/","plan":"Free + Paid","logo":"https://clippit.ai/logo.svg","category":"AI Email Assistance","tags":["email","summaries"],"embeddable":True,"blurb":"Smart email assistance."},  # [web:35]
    {"name":"Friday","link":"https://friday.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/friday.svg","category":"AI Email Assistance","tags":["compose","reply"],"embeddable":True,"blurb":"AI email drafting."},  # [web:35]
    {"name":"Mailmaestro","link":"https://mailmaestro.ai/","plan":"Free + Paid","logo":"https://cdn.prod.website-files.com/66d1d32f08a233fad81d614e/67fd1fefe53c6bbf3b31d62e_maestro-labs-p-500.png","category":"AI Email Assistance","tags":["compose"],"embeddable":True,"blurb":"AI that writes better emails."},  # [web:35]
    {"name":"Shortwave","link":"https://www.shortwave.com/","plan":"Free + Paid","logo":"https://www.shortwave.com/images/logomark.svg","category":"AI Email Assistance","tags":["gmail","ai"],"embeddable":True,"blurb":"Modern email with AI."},  # [web:35]
    {"name":"Superhuman","link":"https://superhuman.com/","plan":"Paid","logo":"https://blog.superhuman.com/content/images/size/w1200/2021/01/Twitter-Card.png","category":"AI Email Assistance","tags":["fast","email"],"embeddable":True,"blurb":"Premium email client with AI."},  # [web:35]

    # -------------------- AI Image Generation --------------------
    {"name":"Adobe Firefly","link":"https://www.adobe.com/products/firefly.html","plan":"Credits + Paid","logo":"https://www.adobe.com/federal/assets/svgs/adobe-logo.svg","category":"AI Image Generation","tags":["adobe","images"],"embeddable":False,"blurb":"Generative AI in Adobe ecosystem."},  # [web:31]
    {"name":"DALL·E","link":"https://openai.com/dall-e-3","plan":"Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/4/4d/OpenAI_Logo.svg","category":"AI Image Generation","tags":["openai","image"],"embeddable":False,"blurb":"Text‑to‑image by OpenAI."},  # [web:24]
    {"name":"FLUX.1","link":"https://blackforestlabs.ai/","plan":"Free + Paid","logo":"https://flux1.ai/logo.svg","category":"AI Image Generation","tags":["bfl","flux"],"embeddable":True,"blurb":"Black Forest Labs image models."},  # [web:35]
    {"name":"Ideogram","link":"https://ideogram.ai/","plan":"Free + Paid","logo":"https://5.imimg.com/data5/SELLER/Default/2024/9/451019279/TC/LH/HV/11701680/ideogram-ai-software.png","category":"AI Image Generation","tags":["text","image"],"embeddable":True,"blurb":"Strong typography generation."},  # [web:35]
    {"name":"Midjourney","link":"https://www.midjourney.com/","plan":"Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/2/24/Midjourney_Emblem.svg","category":"AI Image Generation","tags":["discord","art"],"embeddable":False,"blurb":"High‑quality art generation."},  # [web:33][web:30]
    {"name":"Recraft","link":"https://www.recraft.ai/","plan":"Free + Paid","logo":"https://cdn.prod.website-files.com/655727fe69827d9a402de12c/685e2af1b7ec5f32e053f308_recraft-logo.svg","category":"AI Image Generation","tags":["vector","assets"],"embeddable":True,"blurb":"Design assets with AI."},  # [web:35]
    {"name":"Stable Diffusion","link":"https://stability.ai/","plan":"Free + Paid","logo":"https://stablediffusionweb.com/images/logo.png","category":"AI Image Generation","tags":["sdxl","stability"],"embeddable":True,"blurb":"Open image generation ecosystem."},  # [web:35]


    # -------------------- AI Spreadsheet --------------------
    {"name":"Bricks","link":"https://bricks.so/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/bricks.svg","category":"AI Spreadsheet","tags":["sheets"],"embeddable":True,"blurb":"Spreadsheet AI helpers."},  # [web:35]
    {"name":"Formula Bot","link":"https://www.formulabot.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/formulabot.svg","category":"AI Spreadsheet","tags":["excel","sheets"],"embeddable":True,"blurb":"Generate Excel/Sheets formulas."},  # [web:35]
    {"name":"Gigasheet","link":"https://www.gigasheet.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/gigasheet.svg","category":"AI Spreadsheet","tags":["big data","csv"],"embeddable":True,"blurb":"Analyze big CSVs in the browser."},  # [web:35]
    {"name":"Rows","link":"https://rows.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/rows.svg","category":"AI Spreadsheet","tags":["automation"],"embeddable":True,"blurb":"Modern spreadsheet with integrations."},  # [web:35]
    {"name":"SheetAI","link":"https://www.sheetai.app/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/sheetai.svg","category":"AI Spreadsheet","tags":["sheets","ai"],"embeddable":True,"blurb":"AI functions for Google Sheets."},  # [web:35]

    # -------------------- AI Meeting Notes --------------------
    {"name":"Avoma","link":"https://www.avoma.com/","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/avoma.svg","category":"AI Meeting Notes","tags":["meet","notes"],"embeddable":True,"blurb":"AI meeting assistant."},  # [web:35]
    {"name":"Equal Time","link":"https://equaltime.io/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/equaltime.svg","category":"AI Meeting Notes","tags":["analytics"],"embeddable":True,"blurb":"Meeting analytics and balance."},  # [web:35]
    {"name":"Fathom","link":"https://fathom.video/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/fathom.svg","category":"AI Meeting Notes","tags":["transcribe"],"embeddable":True,"blurb":"Free Zoom notetaker with AI."},  # [web:35]
    {"name":"Fellow","link":"https://www.fellow.app/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/fellow.svg","category":"AI Meeting Notes","tags":["agenda","notes"],"embeddable":True,"blurb":"Meetings, notes, and action items."},  # [web:35]
    {"name":"Fireflies","link":"https://fireflies.ai/","plan":"Free + Paid","logo":"https://fireflies.ai/favicon.ico","category":"AI Meeting Notes","tags":["calls","notes"],"embeddable":True,"blurb":"AI notetaker for meetings."},  # [web:2]
    {"name":"Krisp","link":"https://krisp.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/krisp.svg","category":"AI Meeting Notes","tags":["noise","calls"],"embeddable":True,"blurb":"Noise cancellation and voice tools."},  # [web:35]
    {"name":"Otter","link":"https://otter.ai/","plan":"Free + Paid","logo":"https://otter.ai/favicon.ico","category":"AI Meeting Notes","tags":["transcription"],"embeddable":True,"blurb":"Live transcription and summaries."},  # [web:2]

    # -------------------- AI Workflow Automation --------------------
    {"name":"Integrately","link":"https://integrately.com/","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/integrately.svg","category":"AI Workflow Automation","tags":["automation"],"embeddable":True,"blurb":"1‑click automation for apps."},  # [web:35]
    {"name":"Make","link":"https://www.make.com/","plan":"Free + Paid","logo":"https://www.make.com/favicon.ico","category":"AI Workflow Automation","tags":["scenarios"],"embeddable":True,"blurb":"Visual automation builder."},  # [web:2]
    {"name":"Monday.com","link":"https://monday.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/monday.svg","category":"AI Workflow Automation","tags":["work os"],"embeddable":True,"blurb":"Work OS with automation."},  # [web:35]
    {"name":"n8n","link":"https://n8n.io/","plan":"Free (self-host) + Paid","logo":"https://n8n.io/favicon.ico","category":"AI Workflow Automation","tags":["open source"],"embeddable":True,"blurb":"Open workflow automation."},  # [web:2]
    {"name":"Wrike","link":"https://www.wrike.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/wrike.svg","category":"AI Workflow Automation","tags":["pm"],"embeddable":True,"blurb":"Project management with AI."},  # [web:35]
    {"name":"Zapier","link":"https://zapier.com/","plan":"Free + Paid","logo":"https://zapier.com/favicon.ico","category":"AI Workflow Automation","tags":["integrations"],"embeddable":True,"blurb":"Connect apps and automate workflows."},  # [web:2]

    # -------------------- AI Writing Generation --------------------
    {"name":"Copy.ai","link":"https://www.copy.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/copyai.svg","category":"AI Writing Generation","tags":["marketing"],"embeddable":True,"blurb":"Marketing copy with AI."},  # [web:35]
    {"name":"Grammarly","link":"https://www.grammarly.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/grammarly.svg","category":"AI Writing Generation","tags":["grammar","rewrite"],"embeddable":True,"blurb":"Writing assistant and checker."},  # [web:35]
    {"name":"Jasper","link":"https://www.jasper.ai/","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/jasper.svg","category":"AI Writing Generation","tags":["brand","content"],"embeddable":True,"blurb":"Brand‑safe AI content platform."},  # [web:35]
    {"name":"JotBot","link":"https://www.jotbot.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/jotbot.svg","category":"AI Writing Generation","tags":["assist"],"embeddable":True,"blurb":"Draft faster with AI."},  # [web:35]
    {"name":"Quarkle","link":"https://www.quarkle.io/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/quarkle.svg","category":"AI Writing Generation","tags":["editor"],"embeddable":True,"blurb":"AI writing and research."},  # [web:35]
    {"name":"QuillBot","link":"https://quillbot.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/quillbot.svg","category":"AI Writing Generation","tags":["paraphrase"],"embeddable":True,"blurb":"Paraphrasing and grammar tools."},  # [web:35]
    {"name":"Rytr","link":"https://rytr.me/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/rytr.svg","category":"AI Writing Generation","tags":["copy"],"embeddable":True,"blurb":"AI copywriter for content."},  # [web:35]
    {"name":"Sudowrite","link":"https://www.sudowrite.com/","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/sudowrite.svg","category":"AI Writing Generation","tags":["creative"],"embeddable":True,"blurb":"Creative writing assistant."},  # [web:35]
    {"name":"Writesonic","link":"https://writesonic.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/writesonic.svg","category":"AI Writing Generation","tags":["content"],"embeddable":True,"blurb":"Content generation platform."},  # [web:35]

    # -------------------- AI Scheduling --------------------
    {"name":"Calendly","link":"https://calendly.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/calendly.svg","category":"AI Scheduling","tags":["meet"],"embeddable":True,"blurb":"Scheduling with smart links."},  # [web:35]
    {"name":"Clockwise","link":"https://www.getclockwise.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/clockwise.svg","category":"AI Scheduling","tags":["calendar"],"embeddable":True,"blurb":"Calendar optimization with AI."},  # [web:35]
    {"name":"Motion","link":"https://www.usemotion.com/","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/motion.svg","category":"AI Scheduling","tags":["auto schedule"],"embeddable":True,"blurb":"Plans day and tasks automatically."},  # [web:35]
    {"name":"Reclaim AI","link":"https://reclaim.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/reclaim.svg","category":"AI Scheduling","tags":["habits"],"embeddable":True,"blurb":"Smart time blocking."},  # [web:35]
    {"name":"Taskade","link":"https://www.taskade.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/taskade.svg","category":"AI Scheduling","tags":["tasks"],"embeddable":True,"blurb":"Tasks, docs, chat with AI."},  # [web:35]
    {"name":"Trevor AI","link":"https://www.trevorai.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/trevor.svg","category":"AI Scheduling","tags":["time block"],"embeddable":True,"blurb":"Time-block planner with AI."},  # [web:35]

    # -------------------- AI Knowledge Management --------------------
    {"name":"Mem","link":"https://get.mem.ai/","plan":"Free + Paid","logo":"https://get.mem.ai/favicon.ico","category":"AI Knowledge Management","tags":["notes","memory"],"embeddable":True,"blurb":"AI‑first notes and recall."},  # [web:2]
    {"name":"Notion","link":"https://www.notion.so/","plan":"Free + Paid","logo":"https://upload.wikimedia.org/wikipedia/commons/e/e9/Notion-logo.svg","category":"AI Knowledge Management","tags":["wiki","notes"],"embeddable":True,"blurb":"Workspace with AI writing and Q&A."},  # [web:2]
    {"name":"Tettra","link":"https://tettra.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/tettra.svg","category":"AI Knowledge Management","tags":["wiki"],"embeddable":True,"blurb":"Internal wiki with AI answers."},  # [web:35]

    # -------------------- AI Video Generation --------------------
    {"name":"Descript","link":"https://www.descript.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/descript.svg","category":"AI Video Generation","tags":["edit","overdub"],"embeddable":True,"blurb":"All‑in‑one audio/video editor with AI."},  # [web:35]
    {"name":"Haiper AI","link":"https://haiper.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/haiper.svg","category":"AI Video Generation","tags":["video"],"embeddable":True,"blurb":"Text‑to‑video generation."},  # [web:35]
    {"name":"Invideo AI","link":"https://invideo.io/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/invideo.svg","category":"AI Video Generation","tags":["marketing"],"embeddable":True,"blurb":"Create videos from prompts."},  # [web:35]
    {"name":"Kling","link":"https://klingai.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/kling.svg","category":"AI Video Generation","tags":["video","vfx"],"embeddable":True,"blurb":"High‑fidelity video generation."},  # [web:35]
    {"name":"Krea AI","link":"https://www.krea.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/krea.svg","category":"AI Video Generation","tags":["gen","realtime"],"embeddable":True,"blurb":"Realtime generation and editing."},  # [web:35]
    {"name":"LTX Studio","link":"https://ltx.studio/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/ltx.svg","category":"AI Video Generation","tags":["story"],"embeddable":True,"blurb":"Story‑to‑video platform."},  # [web:35]
    {"name":"Luma AI","link":"https://lumalabs.ai/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/luma.svg","category":"AI Video Generation","tags":["3d","vid"],"embeddable":True,"blurb":"Video and 3D generation."},  # [web:35]
    {"name":"Pika","link":"https://pika.art/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/pika.svg","category":"AI Video Generation","tags":["video"],"embeddable":True,"blurb":"AI video from text."},  # [web:35]
    {"name":"Runway","link":"https://runwayml.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/runway.svg","category":"AI Video Generation","tags":["gen","edit"],"embeddable":True,"blurb":"Gen‑2/Gen‑3 video tools."},  # [web:35]
    {"name":"Sora","link":"https://openai.com/sora","plan":"Paid","logo":"https://ai-logos-svg.vercel.app/logos/sora.svg","category":"AI Video Generation","tags":["openai","video"],"embeddable":False,"blurb":"Text‑to‑video by OpenAI."},  # [web:35]

    # -------------------- AI Graphic Design --------------------
    {"name":"AutoDraw","link":"https://www.autodraw.com/","plan":"Free","logo":"https://ai-logos-svg.vercel.app/logos/autodraw.svg","category":"AI Graphic Design","tags":["sketch"],"embeddable":True,"blurb":"Draw with AI suggestions."},  # [web:35]
    {"name":"Canva","link":"https://www.canva.com/","plan":"Free + Paid","logo":"https://static.canva.com/static/images/favicon.ico","category":"AI Graphic Design","tags":["design","templates"],"embeddable":True,"blurb":"Design anything with templates and AI."},  # [web:2]
    {"name":"Design.com","link":"https://www.design.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/designcom.svg","category":"AI Graphic Design","tags":["logos"],"embeddable":True,"blurb":"Logo and brand design with AI."},  # [web:35]
    {"name":"Framer","link":"https://www.framer.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/framer.svg","category":"AI Graphic Design","tags":["web","design"],"embeddable":True,"blurb":"AI‑assisted web design."},  # [web:35]
    {"name":"Microsoft Designer","link":"https://designer.microsoft.com/","plan":"Free + Paid","logo":"https://designer.microsoft.com/favicon.ico","category":"AI Graphic Design","tags":["image","layout"],"embeddable":True,"blurb":"AI design by Microsoft."},  # [web:2]
    {"name":"Uizard","link":"https://uizard.io/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/uizard.svg","category":"AI Graphic Design","tags":["wireframe","ui"],"embeddable":True,"blurb":"Wireframes and UI from sketches."},  # [web:35]

    # -------------------- AI Data Visualization --------------------
    {"name":"Decktopus","link":"https://www.decktopus.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/decktopus.svg","category":"AI Data Visualization","tags":["decks","charts"],"embeddable":True,"blurb":"AI‑assisted decks and charts."},  # [web:35]
    {"name":"Flourish","link":"https://flourish.studio/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/flourish.svg","category":"AI Data Visualization","tags":["charts"],"embeddable":True,"blurb":"Interactive charts and maps."},  # [web:35]
    {"name":"Visme","link":"https://www.visme.co/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/visme.svg","category":"AI Data Visualization","tags":["infographics"],"embeddable":True,"blurb":"Infographics, presentations, charts."},  # [web:35]
    {"name":"Zing Data","link":"https://www.zingdata.com/","plan":"Free + Paid","logo":"https://ai-logos-svg.vercel.app/logos/zing.svg","category":"AI Data Visualization","tags":["bi","mobile"],"embeddable":True,"blurb":"Mobile‑first BI with AI."},  # [web:35]


    # -------------------- Free AI API Access --------------------
{"name":"Groq","link":"https://groq.com/","plan":"Free + Paid","logo":"https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg","category":"Free AI API Access","tags":["llm","fast-inference","chatbot"],"embeddable":True,"blurb":"Ultra-fast LLM inference. Free: 14,400 requests/day, 30 req/min for Llama models."},

{"name":"OpenRouter","link":"https://openrouter.ai/","plan":"Free + Paid","logo":"https://openrouter.ai/favicon-32x32.png","category":"Free AI API Access","tags":["llm","aggregator","multi-model"],"embeddable":True,"blurb":"Unified API for multiple AI models. Free models available (Llama, Mistral), pay only for premium."},

{"name":"Google Gemini API","link":"https://ai.google.dev/","plan":"Free + Paid","logo":"https://www.gstatic.com/lamda/images/gemini_sparkle_v002_d4735304ff6292a690345.svg","category":"Free AI API Access","tags":["llm","multimodal","google"],"embeddable":True,"blurb":"Multimodal AI from Google. Free: 60 requests/min, 1,500 requests/day for Gemini Pro."},

{"name":"Cohere","link":"https://cohere.com/","plan":"Free + Paid","logo":"https://cohere.com/favicon.ico","category":"Free AI API Access","tags":["nlp","embeddings","generation"],"embeddable":True,"blurb":"Production NLP models. Free: 100 API calls/min, 1000 calls/month trial credits."},

{"name":"Mistral AI","link":"https://mistral.ai/","plan":"Free + Paid","logo":"https://mistral.ai/images/logo_hubc88c4ece131b91c7cb753f40e9e1cc5_2589_256x0_resize_q97_h2_lanczos_3.webp","category":"Free AI API Access","tags":["llm","open-source","europe"],"embeddable":True,"blurb":"European open LLMs. Free: €5 trial credits, rate limits vary by model."},

{"name":"Hugging Face Inference API","link":"https://huggingface.co/inference-api","plan":"Free + Paid","logo":"https://huggingface.co/front/assets/huggingface_logo-noborder.svg","category":"Free AI API Access","tags":["models","inference","open-source"],"embeddable":True,"blurb":"Access 350k+ models. Free: Rate-limited inference, 1000 requests/hour for popular models."},

{"name":"Together AI","link":"https://www.together.ai/","plan":"Free + Paid","logo":"https://www.together.ai/favicon.ico","category":"Free AI API Access","tags":["inference","open-models","fast"],"embeddable":True,"blurb":"Fast open-source model inference. Free: $25 trial credits, ~1M tokens for Llama-3."},

{"name":"Replicate","link":"https://replicate.com/","plan":"Free + Paid","logo":"https://replicate.com/favicon.ico","category":"Free AI API Access","tags":["models","image","video"],"embeddable":True,"blurb":"Run AI models via API. Free: $0.01 trial credits, pay-per-use after (very affordable)."},

{"name":"Ollama","link":"https://ollama.ai/","plan":"Free","logo":"https://ollama.ai/public/icon-32x32.png","category":"Free AI API Access","tags":["local","self-hosted","llm"],"embeddable":False,"blurb":"Run LLMs locally. Free: Unlimited, runs on your hardware with OpenAI-compatible API."},

{"name":"LocalAI","link":"https://localai.io/","plan":"Free","logo":"https://localai.io/favicon.ico","category":"Free AI API Access","tags":["local","self-hosted","openai-compatible"],"embeddable":False,"blurb":"Self-hosted OpenAI alternative. Free: Unlimited, supports 50+ model architectures locally."},

{"name":"Anthropic Claude API","link":"https://www.anthropic.com/api","plan":"Trial + Paid","logo":"https://www.anthropic.com/images/icons/favicon-32x32.png","category":"Free AI API Access","tags":["llm","reasoning","safety"],"embeddable":True,"blurb":"Advanced reasoning AI. Free: $5 trial credits (~1M tokens), then pay-as-you-go."},

{"name":"Stability AI","link":"https://platform.stability.ai/","plan":"Trial + Paid","logo":"https://platform.stability.ai/favicon.ico","category":"Free AI API Access","tags":["image","stable-diffusion","generation"],"embeddable":True,"blurb":"Image generation API. Free: 25 trial credits for Stable Diffusion XL generation."},

{"name":"ElevenLabs","link":"https://elevenlabs.io/","plan":"Free + Paid","logo":"https://elevenlabs.io/favicon.ico","category":"Free AI API Access","tags":["voice","tts","audio"],"embeddable":True,"blurb":"AI voice generation. Free: 10,000 characters/month, 3 custom voices."},

{"name":"AssemblyAI","link":"https://www.assemblyai.com/","plan":"Free + Paid","logo":"https://www.assemblyai.com/favicon.ico","category":"Free AI API Access","tags":["speech-to-text","transcription","audio"],"embeddable":True,"blurb":"Speech-to-text API. Free: $50 trial credits, ~300 hours of transcription."},

{"name":"Deepgram","link":"https://deepgram.com/","plan":"Free + Paid","logo":"https://deepgram.com/favicon.ico","category":"Free AI API Access","tags":["speech-to-text","real-time","audio"],"embeddable":True,"blurb":"Real-time speech recognition. Free: $200 credits, 12,000 minutes of audio processing."},

{"name":"Pinecone","link":"https://www.pinecone.io/","plan":"Free + Paid","logo":"https://www.pinecone.io/favicon.ico","category":"Free AI API Access","tags":["vector-db","embeddings","search"],"embeddable":True,"blurb":"Vector database for AI. Free: 100K vectors, 1 pod, 5 indexes (Starter plan)."},

{"name":"Weaviate","link":"https://weaviate.io/","plan":"Free + Paid","logo":"https://weaviate.io/favicon.ico","category":"Free AI API Access","tags":["vector-db","search","open-source"],"embeddable":True,"blurb":"Open-source vector database. Free: Sandbox 14 days, self-hosted unlimited."},

{"name":"Voyage AI","link":"https://www.voyageai.com/","plan":"Free + Paid","logo":"https://www.voyageai.com/favicon.ico","category":"Free AI API Access","tags":["embeddings","search","rag"],"embeddable":True,"blurb":"State-of-the-art embeddings. Free: 50M tokens/month for retrieval/search tasks."},

{"name":"Jina AI","link":"https://jina.ai/","plan":"Free + Paid","logo":"https://jina.ai/favicon.ico","category":"Free AI API Access","tags":["embeddings","search","multimodal"],"embeddable":True,"blurb":"Multimodal embeddings & search. Free: 1M tokens/month for embedding models."},

{"name":"AI/ML API","link":"https://aimlapi.com/","plan":"Free + Paid","logo":"https://aimlapi.com/favicon.ico","category":"Free AI API Access","tags":["aggregator","multi-model","affordable"],"embeddable":True,"blurb":"200+ AI models in one API. Free: $5.99 trial credits, access to all models."},
]


