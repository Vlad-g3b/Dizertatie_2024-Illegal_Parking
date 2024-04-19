<script>
    export let size = '32px'; // Default size of the spinner
    export let color = '#007bff'; // Default color of the spinner
  </script>
  
  <style>
    .spinner {
      border: 4px solid rgba(0, 0, 0, 0.1);
      border-left-color: var(--color);
      border-radius: 50%;
      width: var(--size);
      height: var(--size);
      animation: spin 1s linear infinite;
    }
  
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  </style>
  
  <div class="spinner" style="--size: {size}; --color: {color}"></div>