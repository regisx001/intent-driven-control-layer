<script lang="ts">
	type ToolTrace = {
		tool: string;
		arguments: Record<string, unknown>;
		result_preview: string;
	};

	type IntentResponse = {
		answer: string;
		model: string;
		tools_used: ToolTrace[];
	};

	type DatasetPreviewResponse = {
		dataset: string;
		preview_markdown: string;
	};

	type DatasetsResponse = {
		count: number;
		datasets: string[];
	};

	let apiBase = $state('http://127.0.0.1:8000');
	let healthMessage = $state('');
	let datasets = $state<string[]>([]);
	let datasetName = $state('energy');
	let nRows = $state(5);
	let previewTitle = $state('');
	let previewMarkdown = $state('');
	let prompt = $state('give me the last 1 row in energy dataset');
	let model = $state('functiongemma');
	let maxSteps = $state(8);
	let intentResult = $state<IntentResponse | null>(null);

	let apiError = $state('');
	let datasetError = $state('');
	let intentError = $state('');

	let checkingHealth = $state(false);
	let loadingDatasets = $state(false);
	let loadingPreview = $state(false);
	let loadingIntent = $state(false);

	function normalizeBaseUrl(url: string): string {
		return url.trim().replace(/\/+$/, '');
	}

	async function requestJson<T>(path: string, options: RequestInit = {}): Promise<T> {
		const baseUrl = normalizeBaseUrl(apiBase);
		if (!baseUrl) {
			throw new Error('API base URL is required.');
		}

		const response = await fetch(`${baseUrl}${path}`, {
			...options,
			headers: {
				'Content-Type': 'application/json',
				...(options.headers ?? {})
			}
		});

		const textPayload = await response.text();
		let jsonPayload: unknown;

		try {
			jsonPayload = textPayload ? JSON.parse(textPayload) : {};
		} catch {
			jsonPayload = { detail: textPayload };
		}

		if (!response.ok) {
			const detail =
				typeof jsonPayload === 'object' && jsonPayload !== null && 'detail' in jsonPayload
					? String((jsonPayload as { detail: unknown }).detail)
					: `Request failed with status ${response.status}`;
			throw new Error(detail);
		}

		return jsonPayload as T;
	}

	function prettyJson(value: unknown): string {
		return JSON.stringify(value, null, 2);
	}

	async function checkHealth(): Promise<void> {
		checkingHealth = true;
		apiError = '';
		healthMessage = '';

		try {
			const data = await requestJson<{ status: string }>('/health');
			healthMessage = data.status;
		} catch (error) {
			apiError = error instanceof Error ? error.message : 'Unable to reach API.';
		} finally {
			checkingHealth = false;
		}
	}

	async function fetchDatasets(): Promise<void> {
		loadingDatasets = true;
		datasetError = '';

		try {
			const data = await requestJson<DatasetsResponse>('/datasets');
			datasets = data.datasets;
			if (data.datasets.length > 0 && !data.datasets.includes(`${datasetName}.csv`)) {
				datasetName = data.datasets[0].replace(/\.csv$/i, '');
			}
		} catch (error) {
			datasetError = error instanceof Error ? error.message : 'Unable to load datasets.';
		} finally {
			loadingDatasets = false;
		}
	}

	async function fetchPreview(kind: 'head' | 'tail'): Promise<void> {
		loadingPreview = true;
		datasetError = '';
		previewMarkdown = '';

		try {
			const endpoint = `/datasets/${encodeURIComponent(datasetName)}${
				kind === 'head' ? '/head' : '/tail'
			}?n_rows=${nRows}`;
			const data = await requestJson<DatasetPreviewResponse>(endpoint);
			previewTitle = `${kind.toUpperCase()} preview - ${data.dataset}`;
			previewMarkdown = data.preview_markdown;
		} catch (error) {
			datasetError = error instanceof Error ? error.message : 'Unable to load preview.';
		} finally {
			loadingPreview = false;
		}
	}

	async function runIntent(): Promise<void> {
		loadingIntent = true;
		intentError = '';
		intentResult = null;

		try {
			const data = await requestJson<IntentResponse>('/intent/query', {
				method: 'POST',
				body: JSON.stringify({
					prompt,
					model,
					max_steps: maxSteps
				})
			});

			intentResult = data;
		} catch (error) {
			intentError = error instanceof Error ? error.message : 'Intent query failed.';
		} finally {
			loadingIntent = false;
		}
	}
</script>

<main class="container-fluid app-shell">
	<header>
		<h1>Intent Control Layer</h1>
		<p>A simple SvelteKit + PicoCSS interface for your FastAPI server.</p>
	</header>

	<section>
		<article>
			<header>
				<h2>API Connection</h2>
			</header>

			<label for="apiBase">FastAPI base URL</label>
			<input id="apiBase" type="url" bind:value={apiBase} placeholder="http://127.0.0.1:8000" />

			<div role="group">
				<button onclick={checkHealth} aria-busy={checkingHealth}>Check health</button>
				<button class="secondary" onclick={fetchDatasets} aria-busy={loadingDatasets}>
					Load datasets
				</button>
			</div>

			{#if healthMessage}
				<p><strong>Health:</strong> {healthMessage}</p>
			{/if}

			{#if apiError}
				<p class="error-text">{apiError}</p>
			{/if}

			{#if datasets.length > 0}
				<details>
					<summary>Available datasets ({datasets.length})</summary>
					<ul>
						{#each datasets as dataset}
							<li>{dataset}</li>
						{/each}
					</ul>
				</details>
			{/if}
		</article>
	</section>

	<section class="grid">
		<article>
			<header>
				<h2>Dataset Preview</h2>
			</header>

			<label for="datasetName">Dataset name</label>
			<input id="datasetName" bind:value={datasetName} placeholder="energy" />

			<label for="rows">Rows</label>
			<input id="rows" type="number" min="1" max="200" bind:value={nRows} />

			<div role="group">
				<button onclick={() => fetchPreview('head')} aria-busy={loadingPreview}>Get head</button>
				<button class="secondary" onclick={() => fetchPreview('tail')} aria-busy={loadingPreview}>
					Get tail
				</button>
			</div>

			{#if datasetError}
				<p class="error-text">{datasetError}</p>
			{/if}

			{#if previewMarkdown}
				<h3>{previewTitle}</h3>
				<div class="overflow-auto">
					<pre>{previewMarkdown}</pre>
				</div>
			{/if}
		</article>

		<article>
			<header>
				<h2>Intent Query</h2>
			</header>

			<label for="prompt">Prompt</label>
			<textarea id="prompt" rows="6" bind:value={prompt}></textarea>

			<div class="grid">
				<label for="model">
					Model
					<input id="model" bind:value={model} />
				</label>

				<label for="maxSteps">
					Max steps
					<input id="maxSteps" type="number" min="1" max="20" bind:value={maxSteps} />
				</label>
			</div>

			<button onclick={runIntent} aria-busy={loadingIntent}>Run intent</button>

			{#if intentError}
				<p class="error-text">{intentError}</p>
			{/if}

			{#if intentResult}
				<h3>Answer</h3>
				<p>{intentResult.answer}</p>

				<details open>
					<summary>Tool trace ({intentResult.tools_used.length})</summary>

					{#if intentResult.tools_used.length === 0}
						<p>No tools were invoked for this request.</p>
					{:else}
						{#each intentResult.tools_used as trace, index}
							<article class="trace-card">
								<header>
									<strong>Step {index + 1}:</strong>
									{trace.tool}
								</header>
								<p>Arguments</p>
								<div class="overflow-auto"><pre>{prettyJson(trace.arguments)}</pre></div>
								<p>Result preview</p>
								<div class="overflow-auto"><pre>{trace.result_preview}</pre></div>
							</article>
						{/each}
					{/if}
				</details>
			{/if}
		</article>
	</section>
</main>
