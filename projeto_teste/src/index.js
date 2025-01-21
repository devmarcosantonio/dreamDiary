const { GoogleGenerativeAI } = require("@google/generative-ai");
const cors = require('cors');  // Importa o middleware cors

const genAI = new GoogleGenerativeAI("AIzaSyBO2yXbZnEef5Gj1B7sSs4ouVhqJEPyC00");
const model = genAI.getGenerativeModel({ model: "gemini-1.5-flash" });

const express = require('express')

const app = express()

// Habilita o CORS para todas as rotas
app.use(cors());

app.post('/interprete', express.json(), async (req, res) => {
    const prompt = `Interprete esse sonho em 2 parágrafos, somente texto: ${req.body.sonho}`;
    try {
        const result = await model.generateContent(prompt);
        const interpretation = result.response?.candidates?.[0]?.content?.parts?.[0]?.text || "Interpretação não disponível.";
        res.send({ interpretacao: interpretation }); 
    } catch (error) {
        console.error('Erro ao gerar conteúdo:', error);
        res.status(500).send({ error: 'Erro ao gerar interpretação.' });
    }
});

app.listen(3000, (error) => {
    if (error) {
        console.log('erro')
        console.log("aqui se kascohusbnd")
    } else {
        console.log('servidor rodando')
    }
})