const express = require("express");
const path = require("path");

const app = express();
const PORT = 8080;

// Serve static files from "public" folder
app.use(express.static(path.join(__dirname, "public")));

app.listen(PORT, () => {
  console.log(`UI app running at http://localhost:${PORT}`);
});
