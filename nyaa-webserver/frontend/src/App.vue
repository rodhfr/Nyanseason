<template>
  <div id="app">
    <h1>Run Python Script via Express</h1>
    <button @click="runPython">Run Python</button>
    <pre v-if="output">{{ output }}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      output: null
    };
  },
  methods: {
    runPython() {
      fetch('http://localhost:3000/run-python')
        .then(response => response.text())
        .then(data => {
          this.output = data; // Store the response in `output`
        })
        .catch(error => {
          this.output = 'Error: ' + error;
        });
    }
  }
};
</script>

<style>
button {
  font-size: 16px;
  padding: 10px;
  background-color: #42b983;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #349a77;
}
pre {
  background-color: #f0f0f0;
  padding: 10px;
  border-radius: 5px;
}
</style>

