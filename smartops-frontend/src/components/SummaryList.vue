<template>
  <div class="card">
    <h2>Summary</h2>
    <div class="summary-content">
      <p>{{ summary }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SummaryList',
  props: {
    summary: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.summary-content {
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-left: 4px solid #1a73e8;
  border-radius: 4px;
}

.summary-content p {
  line-height: 1.6;
  color: #333;
}
</style>
