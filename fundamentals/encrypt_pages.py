#!/usr/bin/env python3
"""
Encrypt the content of password-gated HTML pages with AES-256-GCM.
View Source will show only encrypted gibberish. Decrypted client-side
with Web Crypto API when the correct passphrase is entered.
"""

import os, re, base64, hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PASSPHRASE = "zhenkai123"
ITERATIONS = 100_000

FILES = [
    "pytorch_drills_wed.html",
    "pytorch_drills_thu.html",
    "pytorch_drills_fri.html",
    "pytorch_drills_all.html",
    "story_narratives.html",
    "nuance_onsite_prep.html",
    "wild_research_proposals.html",
]

# The decryption JS that replaces the old gate script
DECRYPT_JS = r"""
<div id="gate" style="display:flex;align-items:center;justify-content:center;height:100vh;background:#0f1220">
  <div style="text-align:center">
    <p style="color:#aab0d5;font-family:system-ui;margin-bottom:12px">This page is encrypted.</p>
    <input id="pw" type="password" placeholder="passphrase" autofocus
      style="padding:10px 16px;border-radius:8px;border:1px solid #252a45;background:#171a2b;color:#e7e9f7;font-size:16px;font-family:system-ui;outline:none;width:220px"
      onkeydown="if(event.key==='Enter')unlock()">
    <br><button onclick="unlock()"
      style="margin-top:10px;padding:8px 24px;border-radius:8px;border:none;background:#7c9cff;color:#0f1220;font-weight:700;cursor:pointer;font-family:system-ui">Enter</button>
    <p id="err" style="color:#ff6b6b;font-family:system-ui;margin-top:8px;display:none">Wrong passphrase</p>
  </div>
</div>
<div id="content-wrap"></div>
<script>
async function unlock(){
  try{
    const pw=document.getElementById('pw').value;
    const blob=document.getElementById('enc-blob').textContent.trim();
    const raw=Uint8Array.from(atob(blob),c=>c.charCodeAt(0));
    const salt=raw.slice(0,16);
    const iv=raw.slice(16,28);
    const ct=raw.slice(28);
    const enc=new TextEncoder();
    const keyMaterial=await crypto.subtle.importKey('raw',enc.encode(pw),{name:'PBKDF2'},false,['deriveKey']);
    const key=await crypto.subtle.deriveKey({name:'PBKDF2',salt,iterations:100000,hash:'SHA-256'},keyMaterial,{name:'AES-GCM',length:256},false,['decrypt']);
    const pt=await crypto.subtle.decrypt({name:'AES-GCM',iv},key,ct);
    const html=new TextDecoder().decode(pt);
    document.getElementById('gate').style.display='none';
    document.getElementById('content-wrap').innerHTML=html;
    document.getElementById('content-wrap').style.display='block';
    sessionStorage.setItem('k_auth_v2',btoa(pw));
  }catch(e){document.getElementById('err').style.display='block'}
}
(async()=>{
  const cached=sessionStorage.getItem('k_auth_v2');
  if(cached){document.getElementById('pw').value=atob(cached);await unlock()}
})();
</script>
<script id="enc-blob" type="text/plain">
"""

def encrypt_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()

    # Check if already encrypted
    if 'enc-blob' in html:
        print(f"  SKIP (already encrypted): {filepath}")
        return

    # Extract the content between content-wrap div
    # Pattern: <div id="content-wrap" style="display:none"> ... </div><!-- optional comment --> before </body> or </div></body>
    # We need to capture everything inside content-wrap

    # Find the start of content-wrap
    m_start = re.search(r'<div\s+id="content-wrap"[^>]*>', html)
    if not m_start:
        print(f"  ERROR: no content-wrap found in {filepath}")
        return

    content_start = m_start.end()

    # Find the old gate div, script, and content-wrap opening
    # We need to replace from <div id="gate"...> through the end of </div></div></body>
    gate_start = html.find('<div id="gate"')
    if gate_start == -1:
        print(f"  ERROR: no gate div found in {filepath}")
        return

    # Find </body> to know where content ends
    body_end = html.rfind('</body>')

    # Everything from after content-wrap opening to the closing </div>s before </body>
    # The content-wrap has nested divs, so we need to find the matching close
    # Strategy: everything between content-wrap start and the last </div> tags before </body>

    # Get the tail of the file from content_start to </body>
    tail = html[content_start:body_end]

    # The content is inside content-wrap, which ends with </div></div><!-- /content-wrap --> or just </div></div>
    # We need to strip the closing tags of content-wrap itself
    # Find the last occurrence of </div> that closes content-wrap
    # Usually pattern is: ...content...</div></div><!-- /content-wrap -->

    # Let's find what comes after the content-wrap closing
    # The content-wrap closing could be </div>\n</div><!-- /content-wrap --> or just </div>\n</div>

    # Simpler approach: extract everything between content-wrap open and </body>,
    # then remove trailing </div> tags that close content-wrap and its wrapper

    # Strip trailing whitespace and </div> tags
    content_region = tail.rstrip()

    # Remove the closing </div> for content-wrap itself
    # Count: content-wrap is one div, so we need to remove one </div> at the end
    # But some files have <!-- /content-wrap --> comment
    content_region = re.sub(r'\s*</div>\s*(?:<!--\s*/content-wrap\s*-->\s*)?$', '', content_region)

    # The plaintext to encrypt
    plaintext = content_region.strip()

    # Encrypt
    salt = os.urandom(16)
    iv = os.urandom(12)
    key = hashlib.pbkdf2_hmac('sha256', PASSPHRASE.encode(), salt, ITERATIONS, dklen=32)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(iv, plaintext.encode('utf-8'), None)

    # Combine: salt + iv + ciphertext (includes GCM tag)
    blob = base64.b64encode(salt + iv + ciphertext).decode('ascii')

    # Rebuild the HTML
    # Keep everything before the gate div (head + styles)
    head_part = html[:gate_start]

    # New body content
    new_body = DECRYPT_JS + blob + "\n</script>\n</body>\n</html>\n"

    new_html = head_part + new_body

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_html)

    print(f"  OK: {filepath} ({len(plaintext)} chars encrypted)")

if __name__ == '__main__':
    base = os.path.dirname(os.path.abspath(__file__))
    for fname in FILES:
        path = os.path.join(base, fname)
        print(f"Processing {fname}...")
        encrypt_file(path)
    print("\nDone. All content is now AES-256-GCM encrypted.")
    print("View Source shows only encrypted gibberish.")
