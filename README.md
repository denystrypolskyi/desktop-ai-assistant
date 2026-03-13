<h1>Desktop Local Voice Assistant</h1>

<p>
A Python-based voice assistant that can control the system, launch applications,
and play music through Spotify using local intent classification with an optional LLM fallback.
</p>



<h2>Key Features</h2>

<ul>
<li>Local intent classification using <b>sentence-transformers</b></li>
<li>Spotify playback control (play, pause, next, search track)</li>
<li>System control (volume, shutdown, restart, sleep)</li>
<li>Application launcher and process management</li>
<li>Voice responses via TTS</li>
<li>LLM fallback when no system command is detected</li>
<li>Wake-word based command routing</li>
</ul>



<h2>Example Commands</h2>

<pre><code>
jarvis play blinding lights
jarvis open spotify
jarvis set volume to 40
jarvis next track
jarvis shutdown computer
</code></pre>



<h2>Architecture</h2>

<pre><code>
User Command
      │
      ▼
Wake Word Detection
      │
      ▼
Intent Classification
(sentence-transformers)
      │
 ┌────┴─────────┐
 │              │
 ▼              ▼
System Command   LLM Fallback
Execution
</code></pre>

<h2>How It Works</h2>

<ul>

<li>
<b>Intent Classification</b><br>
Commands are classified using <code>sentence-transformers</code> with the
<code>all-MiniLM-L6-v2</code> embedding model.  
User input is converted to embeddings and matched against predefined
intent phrases using <b>cosine similarity</b>.
</li>

<li>
<b>Local LLM Fallback</b><br>
If a command does not match any predefined intent, the request is
forwarded to a locally running model via <code>llama.cpp</code>.
</li>

<li>
<b>Example Local Model</b><br>
The assistant can run any GGUF model supported by <code>llama.cpp</code>.
Example lightweight model:

<pre><code>unsloth/Qwen3-0.6B-GGUF</code></pre>

Example command to start the server:

<pre><code>llama-server.exe -hf unsloth/Qwen3-0.6B-GGUF:Q4_K_M</code></pre>

</li>

<li>
<b>Spotify Integration</b><br>
Spotify playback control is implemented using the
<code>Spotipy</code> client for the Spotify Web API.
</li>

<li>
<b>System Control</b><br>
System interaction uses <code>pycaw</code> for volume control,
<code>psutil</code> for process management, and Windows API calls
through <code>ctypes</code>.
</li>

</ul>

