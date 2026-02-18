---
name: document-processing
description: Creation et manipulation de documents (DOCX, PDF, PPTX, XLSX)
---

# Document Processing

## Capacites

Creer, editer et analyser des documents bureautiques
sans dependance a des applications desktop.

## DOCX (Word)

### Creation

```javascript
const { Document, Packer, Paragraph, TextRun } = require('docx');

const doc = new Document({
  sections: [{
    properties: {},
    children: [
      new Paragraph({
        children: [
          new TextRun({ text: "Titre du document", bold: true, size: 28 }),
        ],
      }),
      new Paragraph({
        children: [
          new TextRun("Contenu du paragraphe."),
        ],
      }),
    ],
  }],
});

const buffer = await Packer.toBuffer(doc);
```

### Analyse

- Extraire le texte pur
- Lire les commentaires et le suivi des modifications
- Parser les tableaux et les listes

## PDF

### Creation

```javascript
const PDFDocument = require('pdfkit');

const doc = new PDFDocument();
doc.pipe(fs.createWriteStream('output.pdf'));
doc.fontSize(20).text('Titre', { align: 'center' });
doc.fontSize(12).text('Contenu du document.');
doc.end();
```

### Manipulation

- Fusion de PDFs
- Extraction de pages
- Extraction de texte et tables
- Formulaires PDF (remplissage, lecture)

## XLSX (Excel)

```javascript
const ExcelJS = require('exceljs');

const workbook = new ExcelJS.Workbook();
const sheet = workbook.addWorksheet('Donnees');

sheet.columns = [
  { header: 'Nom', key: 'name', width: 20 },
  { header: 'Montant', key: 'amount', width: 15 },
];

sheet.addRow({ name: 'Item 1', amount: 100 });
sheet.addRow({ name: 'Item 2', amount: 200 });

// Formule
sheet.getCell('B4').value = { formula: 'SUM(B2:B3)' };

await workbook.xlsx.writeFile('output.xlsx');
```

## PPTX (PowerPoint)

```javascript
const pptxgen = require('pptxgenjs');

const pres = new pptxgen();
const slide = pres.addSlide();

slide.addText('Titre de la presentation', {
  x: 1, y: 1, w: 8, h: 1.5,
  fontSize: 24, bold: true, align: 'center'
});

slide.addText('Point cle du slide', {
  x: 1, y: 3, w: 8, h: 1,
  fontSize: 14, bullet: true
});

await pres.writeFile('output.pptx');
```

## Quand utiliser

- Generation de rapports automatises
- Export de donnees dans des formats business
- Traitement de documents entrants
- Templates de documents
