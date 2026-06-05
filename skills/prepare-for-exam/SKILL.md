---
name: prepare-for-exam
description: Convert PDF documents to interactive exam preparation materials. Generates questions per document and cross-document questions for related content. Produces Markdown and HTML output with navigation and progress tracking. Use when user wants to create exam questions from PDF course materials. Examples: "create exam questions from these PDFs", "convert PDFs to study guide", "generate questions from course notes", "make interactive HTML from PDFs"
---

# Prepare for Exam

Convert PDF documents into interactive exam preparation materials with questions, answers, and cross-document correlations.

## Overview

| Capability | Description |
|------------|-------------|
| PDF Conversion | Convert PDFs to Markdown using markitdown |
| Question Generation | Create questions per document (configurable) |
| Cross-Document Questions | Generate questions linking related content |
| HTML Output | Interactive HTML with show/hide answers |
| Navigation | Multi-page navigation between sections |
| Progress Tracking | LocalStorage-based progress persistence |

## When to Use This Skill

Use this skill when:
- User provides PDF documents and asks for exam preparation materials
- User wants to create study questions from course notes
- User requests conversion of course materials to interactive format
- User asks for cross-document question generation

## Workflow

### 1. Convert PDFs to Markdown

```bash
uvx "markitdown[pdf]" <input.pdf> > <output.md>
```

Convert each PDF in the provided location to Markdown format.

### 2. Analyze Content

For each converted Markdown file:
- Identify main topics and sections
- Extract key concepts, definitions, frameworks
- Note relationships between documents
- Recognize case studies and examples

### 3. Generate Questions

**Per Document Questions (default: 10)**

Create exam-style questions for each document:

| Question Type | Purpose |
|---------------|---------|
| Definition | Key terms and concepts |
| Explanation | Frameworks and models |
| Comparison | Compare/contrast concepts |
| Application | Apply knowledge to scenarios |
| Analysis | Deep understanding of relationships |

**Question Format:**

```markdown
**Vraag N:** [Question text]?

<details>
<summary>Toon antwoord</summary>

[Answer content]

</details>
```

**Cross-Document Questions**

When documents are related (same course, related topics):
- Generate questions that connect concepts across documents
- Focus on synthesis and integration of knowledge
- Default: 10 cross-document questions

### 4. Create Markdown Output

Structure the Markdown file:

```markdown
# [Title] - Examenvoorbereiding

## Inhoud

1. [Section 1](#section-1)
2. [Section 2](#section-2)
...

---

## Section 1

### Vragen

**Vraag 1:** [Question]?

<details>
<summary>Toon antwoord</summary>

[Answer]

</details>

---

## Tips en Advies

[Study tips, important concepts, exam preparation advice]
```

### 5. Create HTML Output

Generate interactive HTML files:

**File Structure:**

```
output-folder/
├── index.html          # Navigation page
├── style.css           # Styles
├── script.js           # Progress tracking
├── section1.html       # Questions for section 1
├── section2.html       # Questions for section 2
├── ...
├── cross.html          # Cross-document questions
└── tips.html           # Study tips
```

**Key Features:**

| Feature | Implementation |
|---------|---------------|
| Show/Hide Answers | Toggle buttons with CSS |
| Navigation | Top nav + prev/next buttons |
| Progress Tracking | LocalStorage persistence |
| Responsive | Mobile-friendly design |

### 6. Quality Checks

Validate output:
- [ ] All questions have answers
- [ ] Cross-references are valid
- [ ] HTML navigation works
- [ ] Progress tracking functions
- [ ] Responsive on mobile

## Configuration

| Parameter | Default | Description |
|-----------|---------|-------------|
| questions_per_doc | 10 | Number of questions per document |
| cross_questions | 10 | Number of cross-document questions |
| language | document | Question language (matches source) |
| output_format | both | markdown, html, or both |

## Common Issues

| Issue | Solution |
|-------|----------|
| PDF conversion fails | Check markitdown installation, verify PDF is readable |
| Large file size | Split into multiple HTML pages |
| Missing cross-document links | Verify document relationships |
| Progress not persisting | Check localStorage permissions |

## Example Usage

**Input:**
```
Convert PDFs in ./course-notes/ to exam preparation materials.
```

**Process:**
1. Convert all PDFs in ./course-notes/ to Markdown
2. Generate 10 questions per document
3. Create 10 cross-document questions
4. Output Markdown file and HTML folder

**Input with options:**
```
Create 15 questions per PDF from ./notes/, HTML output only.
```

## Output Artifacts

### Markdown File

- Complete question set in one file
- Table of contents with links
- Cross-document questions section
- Tips and study advice

### HTML Folder

- Interactive multi-page format
- Show/hide answers functionality
- Navigation between sections
- Progress tracking with localStorage
- Responsive design

## Related Skills

- researcher - For additional content research
- python-developer - For complex HTML generation scripts
