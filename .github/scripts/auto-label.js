#!/usr/bin/env node

const { execSync, execFileSync } = require('child_process');

// Configuration based on actual repository labels
const CONFIG = {
  // Core Classification Labels (max 3 per issue)
  labels: {
    bug: {
      keywords: [
        'bug', 'error', 'issue', 'problem', 'broken', 'crash', 'fail', 'exception',
        'wrong', 'incorrect', 'not working', 'doesn\'t work', 'fix', 'defect', 'glitch',
        'unexpected behavior', 'misbehaving', 'malfunction', 'flaw', 'mistake', 'typo',
        'regression', 'crashes', 'freezes', 'hangs', 'stuck', 'infinite loop',
        'timeout', 'connection failed', 'access denied', 'permission error', '404', '500',
        'syntax error', 'runtime error', 'compile error', 'build failed', 'test failed',
        'missing', 'absent', 'not visible', 'hidden', 'not shown', 'disappears',
        'no button', 'button missing', 'not displayed', 'not rendered', 'not appearing',
        'security', 'vulnerability', 'authorization', 'access control', 'idor', 'insecure',
        'broken access control', 'permission bypass', 'unauthorized', 'security flaw',
        'forging', 'forged', 'manipulate', 'bypass', 'exploit', 'attack'
      ],
      weight: 0.4,
      description: 'Something isn\'t working'
    },
    enhancement: {
      keywords: [
        'feature', 'add', 'new', 'implement', 'create', 'support', 'enhancement', 'improve',
        'extend', 'request', 'would like', 'wish', 'suggest', 'proposal', 'idea', 'addition',
        'functionality', 'capability', 'option', 'setting', 'config', 'parameter', 'argument',
        'extend', 'expand', 'upgrade', 'modernize', 'enhance', 'better', 'more', 'additional',
        'extra', 'include', 'incorporate', 'integrate', 'combine', 'merge', 'unify'
      ],
      weight: 0.4,
      description: 'New feature or request'
    },
    documentation: {
      keywords: [
        'doc', 'documentation', 'readme', 'guide', 'manual', 'tutorial', 'explain', 'clarify',
        'instructions', 'how to', 'getting started', 'setup', 'installation', 'usage', 'example',
        'examples', 'demo', 'walkthrough', 'documentation update', 'doc fix', 'readme update',
        'guide update', 'manual update', 'tutorial update', 'api docs', 'api documentation',
        'reference', 'specification', 'specs', 'docs', 'documented', 'undocumented'
      ],
      weight: 0.3,
      description: 'Improvements or additions to documentation'
    },
    question: {
      keywords: [
        'question', 'how', 'what', 'why', 'help', 'clarify', 'explain', 'unclear', 'confused',
        'don\'t understand', 'not sure', 'wondering', 'curious', 'asking', 'inquiry', 'query',
        'how do i', 'what is', 'why does', 'when will', 'where can', 'can someone', 'please help',
        'need assistance', 'guidance needed', 'advice', 'recommendation', 'suggestion needed'
      ],
      weight: 0.2,
      description: 'Further information is requested'
    }
  },

  // Technology Labels
  technology: {
    python: {
      keywords: [
        'python', 'pip', 'pipenv', 'virtualenv', 'requirements.txt', 'setup.py', 'pyproject.toml',
        'import', 'from', 'def', 'class', 'self', '__init__', '__main__', 'if __name__',
        'pandas', 'numpy', 'django', 'flask', 'fastapi', 'requests', 'beautifulsoup', 'scrapy',
        'jupyter', 'notebook', '.py', '.pyc', '.pyo', 'pycache', 'venv', 'env'
      ],
      files: ['*.py', 'requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile'],
      weight: 0.3,
      description: 'Pull requests that update Python code'
    },
    javascript: {
      keywords: [
        'javascript', 'js', 'node', 'npm', 'yarn', 'package.json', 'package-lock.json',
        'yarn.lock', 'react', 'vue', 'angular', 'express', 'koa', 'next.js', 'nuxt.js',
        'function', 'const', 'let', 'var', 'arrow function', 'async', 'await', 'promise',
        'callback', 'dom', 'browser', 'frontend', 'client-side', 'es6', 'es2015', 'typescript'
      ],
      files: ['*.js', '*.jsx', '*.ts', '*.tsx', 'package.json', 'yarn.lock'],
      weight: 0.3,
      description: 'Pull requests that update Javascript code'
    },
    elixir: {
      keywords: [
        'elixir', 'phoenix', 'ecto', 'mix', '.ex', '.exs', 'liveview', 'plug', 'cowboy',
        'gen_server', 'supervisor', 'application', 'otp', 'beam', 'erlang', 'defmodule', 'defp',
        'defmacro', 'pipe', 'pattern matching', 'guard', 'struct', 'protocol', 'behaviour',
        'genserver', 'agent', 'task', 'supervision tree', 'hot code reload', 'iex', 'mix.exs',
        'heex', '.heex', 'live_component', 'live_socket', 'phoenix.live_view', 'assign',
        'socket', 'endpoint', 'route', 'controller', 'view', 'template', 'render'
      ],
      files: ['*.ex', '*.exs', '*.heex', 'mix.exs', 'lib/*_web/*', 'lib/*_web/controllers/*', 'lib/*_web/views/*', 'lib/*_web/templates/*'],
      weight: 0.3,
      description: 'Pull requests that update elixir code'
    },
    docker: {
      keywords: [
        'docker', 'container', 'dockerfile', 'docker-compose', 'docker-compose.yml', 'docker-compose.yaml',
        'containerize', 'containerization', 'docker build', 'docker run', 'docker push', 'docker pull',
        'image', 'registry', 'hub.docker.com', 'docker hub', 'alpine', 'ubuntu', 'scratch',
        'multi-stage', 'layer', 'cache', 'volume', 'mount', 'port', 'expose', 'env'
      ],
      files: ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml', '*.dockerfile'],
      weight: 0.3,
      description: 'Pull requests that update Docker code'
    },
    'github_actions': {
      keywords: [
        'github actions', 'workflow', 'yml', 'yaml', '.github/workflows', 'ci', 'cd', 'continuous',
        'integration', 'deployment', 'pipeline', 'automation', 'trigger', 'event', 'on push',
        'on pull_request', 'steps', 'jobs', 'runs-on', 'uses', 'with', 'secrets', 'env',
        'matrix', 'strategy', 'artifact', 'cache', 'checkout', 'setup-node', 'setup-python',
        'docker build', 'deploy', 'test', 'lint', 'build', 'release', 'publish'
      ],
      files: ['.github/workflows/*.yml', '.github/workflows/*.yaml'],
      weight: 0.3,
      description: 'Pull requests that update GitHub Actions'
    }
  },

  // Component Labels
  components: {
    'copi.owasp.org': {
      keywords: [
        'copi', 'threat dragon', 'threat model', 'threatmodeling', 'threat modeling',
        'threatdragon', 'copi.owasp.org', 'copi owasp', 'threat analysis', 'risk assessment',
        'security model', 'attack tree', 'mitre', 'attack patterns', 'security threats',
        'threat intelligence', 'risk management', 'security architecture', 'threat library',
        'game', 'app', 'application', 'player', 'scores', 'game ends', 'player page',
        'share button', 'copy url', 'liveview', 'show.html', 'player_live', 'game page',
        'multiplayer', 'invite', 'threat dragon app'
      ],
      files: ['copi.owasp.org/*', 'copi/*'],
      weight: 0.3,
      description: 'COPI component issues'
    },
    'cornucopia.owasp.org': {
      keywords: [
        'cornucopia', 'card game', 'deck', 'cards', 'owasp cornucopia', 'cornucopia.owasp.org',
        'security cards', 'threat cards', 'security deck', 'owasp cards', 'game cards',
        'card template', 'deck template', 'card design', 'card layout', 'playing cards',
        'card game mechanics', 'card categories', 'card types', 'card printing',
        'cornucopia cards', 'owasp cornucopia cards', 'security card game'
      ],
      files: ['cornucopia.owasp.org/*', 'cornucopia/*'],
      weight: 0.3,
      description: 'Cornucopia website issues'
    },
    testing: {
      keywords: [
        'test', 'testing', 'tests', 'spec', 'specs', 'unit test', 'integration test', 'e2e test',
        'functional test', 'regression test', 'performance test', 'load test', 'stress test',
        'test coverage', 'coverage', 'jest', 'mocha', 'jasmine', 'karma', 'pytest', 'unittest',
        'rspec', 'minitest', 'test suite', 'test runner', 'assert', 'expect', 'should', 'mock'
      ],
      files: ['*test*', '*spec*', 'test/*', 'tests/*', '__tests__/*', 'spec/*'],
      weight: 0.2,
      description: 'Testing related changes'
    },
    translation: {
      keywords: [
        'translation', 'translate', 'i18n', 'internationalization', 'localization', 'locale',
        'gettext', '.po', '.pot', '.mo', 'locale files', 'language files', 'multi-language',
        'bilingual', 'multilingual', 'translation files', 'translate to', 'localized',
        'check_translations', 'language codes', 'lang_names', 'no_nb', 'pt_br', 'no-nb', 'pt-br',
        'language en', 'language es', 'language fr', 'language de', 'language ja',
        'language zh', 'language ru', 'language pt', 'language it', 'lang en', 'lang es',
        'lang fr', 'lang de', 'lang ja', 'lang zh', 'lang ru', 'lang pt', 'lang it'
      ],
      files: ['*.po', '*.pot', '*.mo', 'locale/*', 'i18n/*', 'lang/*', 'translations/*', 'scripts/check_translations.py'],
      weight: 0.1,
      description: 'Translation and localization changes'
    },
    'good first issue': {
      keywords: [
        'good first issue', 'beginner', 'starter', 'easy', 'simple', 'typo', 'documentation fix',
        'small change', 'minor fix', 'trivial', 'straightforward', 'good first bug',
        'first contribution', 'newcomer', 'first timer', 'getting started', 'introductory',
        'low complexity', 'quick fix', 'simple change', 'beginner friendly'
      ],
      weight: 0.2,
      description: 'Good for newcomers'
    }
  },

  // Configuration
  confidenceThreshold: 0.7,
  maxLabels: 3
};

class AutoLabeler {
  constructor() {
    this.repo = process.env.REPO;
    this.issueNumber = process.env.ISSUE_NUMBER;
    this.dryRun = process.env.DRY_RUN === 'true';
    this.confidenceThreshold = CONFIG.confidenceThreshold;
  }

  async run() {
    try {
      console.log(`🏷️  Auto-labeling issue #${this.issueNumber} in ${this.repo}`);

      if (this.dryRun) {
        console.log('🔍 DRY RUN MODE - No actual changes will be made');
      }

      const issueData = await this.getIssueData();
      const analysis = this.analyzeIssue(issueData);
      const labels = this.generateLabels(analysis);

      console.log('\n📊 Analysis Results:');
      console.log('Labels:', analysis.labels);
      console.log('Technology:', analysis.technology);
      console.log('Components:', analysis.components);
      console.log('Meta:', analysis.meta);
      console.log('Confidence:', analysis.confidence);

      if (labels.length > 0) {
        console.log('\n🏷️  Labels to apply:', labels.join(', '));

        if (!this.dryRun) {
          await this.applyLabels(labels);
          console.log('✅ Labels applied successfully!');
        }
      } else {
        console.log('\n❌ No confident labels generated');
        await this.applyFallbackLabel();
      }

    } catch (error) {
      console.error('❌ Error:', error.message);
      process.exit(1);
    }
  }

  async getIssueData() {
    const args = [
      'issue', 'view', this.issueNumber,
      '--repo', this.repo,
      '--json', 'title,body,labels'
    ];

    const output = execFileSync('gh', args, { encoding: 'utf8' });
    return JSON.parse(output);
  }

  analyzeIssue(issue) {
    const text = `${issue.title} ${issue.body ?? ''}`.toLowerCase();

    const analysis = {
      labels: this.classifyLevel(text, CONFIG.labels),
      technology: this.classifyLevel(text, CONFIG.technology),
      components: this.classifyLevel(text, CONFIG.components)
    };

    // Calculate overall confidence
    const allScores = [
      ...Object.values(analysis.labels),
      ...Object.values(analysis.technology),
      ...Object.values(analysis.components)
    ];
    analysis.confidence = Math.max(...allScores);

    return analysis;
  }

  classifyLevel(text, levelConfig) {
    const scores = {};

    for (const [label, config] of Object.entries(levelConfig)) {
      let score = 0;
      let matchCount = 0;

      // Enhanced keyword matching with weighted scoring
      if (config.keywords) {
        for (const keyword of config.keywords) {
          if (text.includes(keyword.toLowerCase())) {
            // Higher weight for exact phrase matches
            if (keyword.includes(' ')) {
              score += (config.weight || 0.1) * 1.5;
            } else {
              score += config.weight || 0.1;
            }
            matchCount++;
          }
        }

        // Bonus for multiple keyword matches
        if (matchCount > 1) {
          score *= (1 + matchCount * 0.1);
        }
      }

      // File path matching with higher weight
      if (config.files) {
        for (const filePattern of config.files) {
          const normalizedPattern = filePattern.toLowerCase();
          const normalizedText = text.toLowerCase();

          // Check for pattern matches (handle both *.py and **/*.py patterns)
          if (normalizedText.includes(normalizedPattern) ||
            normalizedText.includes(filePattern.replaceAll('*', '').toLowerCase())) {
            score += 0.3;
            matchCount++;
          }
        }
      }

      // Contextual bonuses
      if (label === 'enhancement' && text.includes('feature request')) {
        score += 0.5;
      }
      if (label === 'bug' && (text.includes('reproduce') || text.includes('steps to reproduce'))) {
        score += 0.3;
      }
      if (label === 'documentation' && (text.includes('readme') || text.includes('doc'))) {
        score += 0.3;
      }
      if (label === 'github_actions' && text.includes('workflow')) {
        score += 0.4;
      }
      if (label === 'bug' && (text.includes('security') || text.includes('vulnerability') || text.includes('authorization') || text.includes('access control') || text.includes('idor') || text.includes('insecure'))) {
        score += 0.6;
      }
      if (label === 'bug' && (text.includes('forging') || text.includes('forged') || text.includes('bypass') || text.includes('unauthorized'))) {
        score += 0.5;
      }
      if (label === 'elixir' && (text.includes('liveview') || text.includes('heex') || text.includes('show.html'))) {
        score += 0.5;
      }
      if (label === 'cornucopia.owasp.org' && (text.includes('card game') || text.includes('deck') || text.includes('cards'))) {
        score += 0.4;
      }
      if (label === 'copi.owasp.org' && (text.includes('game') || text.includes('app') || text.includes('application') || text.includes('player') || text.includes('scores'))) {
        score += 0.4;
      }

      // Normalize score to prevent inflation
      scores[label] = Math.min(score, 2.0);
    }

    return scores;
  }

  generateLabels(analysis) {
    const labels = [];

    // Collect all labels with confidence >= threshold
    const allCandidates = [
      ...Object.entries(analysis.labels).map(([label, score]) => ({ label, score, category: 'labels' })),
      ...Object.entries(analysis.technology).map(([label, score]) => ({ label, score, category: 'technology' })),
      ...Object.entries(analysis.components).map(([label, score]) => ({ label, score, category: 'components' }))
    ].filter(item => item.score >= this.confidenceThreshold);

    // Sort by score (descending) and take top 3
    allCandidates.sort((a, b) => b.score - a.score);
    const topLabels = allCandidates.slice(0, CONFIG.maxLabels || 3);

    return topLabels.map(item => item.label);
  }

  async applyLabels(labels) {
    const args = [
      'issue', 'edit', this.issueNumber.toString(),
      '--repo', this.repo,
      '--add-label', labels.join(',')
    ];

    execFileSync('gh', args, { encoding: 'utf8' });
  }

  async applyFallbackLabel() {
    console.log('🏷️  Applying fallback label: needs-triage');
    if (!this.dryRun) {
      const args = [
        'issue', 'edit', this.issueNumber.toString(),
        '--repo', this.repo,
        '--add-label', 'needs-triage'
      ];

      execFileSync('gh', args, { encoding: 'utf8' });
    }
  }
}

// Run the auto-labeler
if (require.main === module) {
  (async () => {
    try {
      const labeler = new AutoLabeler();
      await labeler.run();
    } catch (error) {
      console.error('❌ Auto-labeling failed:', error.message);
      process.exit(1);
    }
  })();
}

module.exports = AutoLabeler;
