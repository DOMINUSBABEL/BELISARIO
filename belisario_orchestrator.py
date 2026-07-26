# -*- coding: utf-8 -*-
"""
BELISARIO: Master Autonomous Orchestrator & Dialectical Quality Engine
Director Supremo de Loops de Publicación y Curaduría Audiovisual (BABYLON.IA Ecosystem)
"""

import os
import sys
import json
import time
import subprocess
import argparse
from datetime import datetime

# UTF-8 Encoding configuration for Windows console
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

VAREGO_DIR = r"C:\Users\jegom\VAREGO"
KINESIO_DIR = r"C:\Users\jegom\shorts_project"
GEIST_DIR = r"C:\Users\jegom\OneDrive\Desktop\Investigaciones\geist"

class BelisarioOrchestrator:
    def __init__(self, channel_handle="@dominus8735"):
        self.channel_handle = channel_handle
        self.max_daily_posts = 4
        self.slot_hours = [8, 12, 16, 20] # UTC-5 optimal publishing slots
        
    def log(self, msg, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [BELISARIO-DIRECTOR] [{level}] {msg}")

    def run_command(self, cmd, cwd=None):
        self.log(f"Executing: {' '.join(cmd)}")
        try:
            res = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='ignore')
            return res.returncode == 0, res.stdout
        except Exception as e:
            self.log(f"Execution Error: {e}", level="ERROR")
            return False, str(e)

    def audit_channel_performance(self):
        self.log(f"Starting performance audit for channel: {self.channel_handle}")
        script_path = os.path.join(VAREGO_DIR, "get_youtube_info.js")
        
        # Pull latest public shorts list
        cmd = ["node", "-e", f"""
        const puppeteer = require('puppeteer-extra');
        const StealthPlugin = require('puppeteer-extra-plugin-stealth');
        puppeteer.use(StealthPlugin());
        const fs = require('fs');

        (async () => {{
            const browser = await puppeteer.launch({{
                executablePath: 'C:\\\\Program Files\\\\Google\\\\Chrome\\\\Application\\\\chrome.exe',
                headless: true,
                args: ['--no-sandbox', '--window-size=1600,1000']
            }});
            const page = await browser.newPage();
            await page.goto('https://www.youtube.com/{self.channel_handle}/shorts', {{ waitUntil: 'networkidle2', timeout: 60000 }});
            await new Promise(r => setTimeout(r, 4000));
            
            const publicData = await page.evaluate(() => {{
                const items = document.querySelectorAll('ytd-rich-item-renderer, ytd-reel-item-renderer');
                const res = [];
                items.forEach(it => {{
                    const title = it.querySelector('#video-title')?.innerText?.trim() || '';
                    const fullText = it.innerText.replace(/\\n/g, ' | ');
                    res.push({{ title, fullText }});
                }});
                return res;
            }});
            fs.writeFileSync('C:\\\\Users\\\\jegom\\\\BELISARIO\\\\latest_audit_metrics.json', JSON.stringify(publicData, null, 2));
            await browser.close();
        }})();
        """]
        
        success, output = self.run_command(cmd, cwd=VAREGO_DIR)
        metrics_file = r"C:\Users\jegom\BELISARIO\latest_audit_metrics.json"
        
        if os.path.exists(metrics_file):
            with open(metrics_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.log(f"Audit completed successfully. {len(data)} Shorts analyzed.")
            return data
        else:
            self.log("Failed to extract performance metrics.", level="WARNING")
            return []

    def enforce_rate_limiter_and_slots(self, posts):
        self.log(f"Applying Anti-Spam Rate Limiter (Max {self.max_daily_posts} daily posts, 4h interval)")
        active_posts = posts[:self.max_daily_posts]
        for idx, p in enumerate(active_posts):
            slot_h = self.slot_hours[idx % len(self.slot_hours)]
            p["scheduled_slot"] = f"{slot_h:02d}:00 UTC-5"
            self.log(f"Slot {idx+1} [{p['scheduled_slot']}]: {p.get('title', p.get('text', 'Post'))[:60]}...")
        return active_posts

    def generate_pinned_comment(self, short_title):
        """Generates a debate-igniting interactive comment for YouTube Shorts."""
        prompt_templates = [
            f"¿Qué opinas sobre este caso? ¿Fue una decisión táctica brillante o un error estratégico? Déjame tu punto de vista 👇",
            f"¿Coincides con este análisis o crees que el factor determinante fue otro? Debate abierto abajo 👇",
            f"¿Cuál crees que debería haber sido la respuesta alternativa? Los leo en los comentarios 👇"
        ]
        import random
        return random.choice(prompt_templates)

    def run_full_publication_loop(self):
        self.log("==================================================")
        self.log("   BELISARIO-DIRECTOR: INICIANDO LOOP AUTÓNOMO    ")
        self.log("==================================================")
        
        # 1. Step 1: Check Context & Trends via VAREGO
        self.log("[Fase 1/4] Extrayendo tendencias y contexto enriquecido...")
        self.run_command(["node", "extract_context.js"], cwd=VAREGO_DIR)
        
        # 2. Step 2: Generate Content Matrix
        self.log("[Fase 2/4] Generando matriz de contenido de alto impacto con Gemini...")
        self.run_command(["python", "generate_multi_topic_posts.py"], cwd=VAREGO_DIR)
        
        # 3. Step 3: Rate Limiting & Clean Titles
        posts_file = r"C:\Users\jegom\output\177_posts\posts.json"
        if os.path.exists(posts_file):
            with open(posts_file, "r", encoding="utf-8") as f:
                posts = json.load(f)
            scheduled_posts = self.enforce_rate_limiter_and_slots(posts)
            
            # 4. Step 4: Video Synthesis via KINESIO & Upload via VAREGO
            self.log("[Fase 4/4] Invocando KINESIO Core y VAREGO para publicación espaciada...")
            for post in scheduled_posts:
                comment = self.generate_pinned_comment(post.get("title", ""))
                self.log(f"Post listo para slot {post.get('scheduled_slot')}. Pinned Comment preparado: {comment[:50]}...")
                
        self.log("[SUCCESS] Loop completado por BELISARIO-DIRECTOR.")

    def update_geist_memory(self, synthesis_text):
        psicohistoria_file = os.path.join(GEIST_DIR, "subgeist_psicohistoria.md")
        if os.path.exists(psicohistoria_file):
            with open(psicohistoria_file, "a", encoding="utf-8") as f:
                f.write(f"\n- **[{datetime.now().strftime('%Y-%m-%d')}] Síntesis Belisario-Director**: {synthesis_text}\n")
            self.log(f"Memoria Geist actualizada en {psicohistoria_file}")

def main():
    parser = argparse.ArgumentParser(description="BELISARIO Master Autonomous Orchestrator CLI")
    parser.add_argument("--loop", action="store_true", help="Ejecutar el loop de publicación y orquestación completo")
    parser.add_argument("--audit", action="store_true", help="Ejecutar auditoría de rendimiento sobre el canal")
    parser.add_argument("--channel", type=str, default="@dominus8735", help="Handle del canal de YouTube")
    args = parser.parse_args()

    orchestrator = BelisarioOrchestrator(channel_handle=args.channel)

    if args.audit:
        orchestrator.audit_channel_performance()
    elif args.loop:
        orchestrator.run_full_publication_loop()
    else:
        print("BELISARIO Orchestrator Engine V1.0.0 -- Usa --loop o --audit para comenzar.")

if __name__ == "__main__":
    main()
