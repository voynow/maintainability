document.addEventListener('DOMContentLoaded', () => {
  showLoginScreen();
});

function showLoginScreen() {
  const root = document.getElementById('root');
  root.innerHTML = `
    <div class='flex items-center justify-center h-full'>
      <div class='p-8 bg-white rounded-lg shadow-md w-1/3 text-center'>
        <h1 class='text-2xl mb-4'>Login</h1>
        <button id='loginBtn' class='p-3 w-full bg-green-500 text-white rounded'>Login</button>
      </div>
    </div>`;
  document.getElementById('loginBtn').addEventListener('click', showMainPage);
}

function showMainPage() {
  const root = document.getElementById('root');
  root.innerHTML = `
    <div class='flex flex-col h-full p-8 bg-white rounded-lg shadow-md w-full'>
      <nav class='mb-4 flex justify-between items-center'>
        <button id='homeBtn'>
          <svg xmlns='http://www.w3.org/2000/svg' class='h-6 w-6' fill='none' viewBox='0 0 24 24' stroke='currentColor'>
            <path strokeLinecap='round' strokeLinejoin='round' strokeWidth={2} d='M3 12l2-2m0 0l7-7 7 7M5 10h14M5 10l2 2m12-2l-2 2' />
          </svg>
        </button>
        <div>
          <button id='apiKeysBtn' class='mr-4'>API Keys</button>
          <button id='paymentsBtn' class='mr-4'>Payments</button>
          <button id='profileBtn'>Profile</button>
        </div>
      </nav>
      <div id='content' class='flex flex-col items-center'></div>
    </div>`;
  document.getElementById('apiKeysBtn').addEventListener('click', showAPIKeysPage);
  document.getElementById('paymentsBtn').addEventListener('click', showPaymentsPage);
  document.getElementById('profileBtn').addEventListener('click', showProfilePage);
  document.getElementById('homeBtn').addEventListener('click', showMainPage);
  showAnalyticsPage();
}
function showAnalyticsPage() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <h1 class='text-2xl mb-4'>Analytics</h1>
    <div class='h-96 bg-gray-200 rounded-lg w-1/2'>
      <!-- Insert Chart Here -->
    </div>`;
}

function showAPIKeysPage() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <h1 class='text-2xl mb-4'>API Keys</h1>
    <div>
      <button id='generateKeyBtn' class='p-2 mb-4 bg-blue-500 text-white rounded'>Generate Key</button>
      <div id='keysList'></div>
    </div>`;
}

function showPaymentsPage() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <h1 class='text-2xl mb-4'>Payments</h1>
    <div>
      <button id='initiatePaymentBtn' class='p-2 mb-4 bg-green-500 text-white rounded'>Initiate Payment</button>
      <div id='subscriptionStatus'></div>
    </div>`;
}

function showProfilePage() {
  const content = document.getElementById('content');
  content.innerHTML = `
    <h1 class='text-2xl mb-4'>Profile</h1>
    <div>
      <div>Email: <span id='email'></span></div>
      <div>API Keys: <span id='apiKeys'></span></div>
      <div>Subscription Status: <span id='subscriptionStatus'></span></div>
    </div>`;
}
