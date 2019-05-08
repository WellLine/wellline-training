import React from 'react';
import logo from './logo.svg';
import './App.css';

function App(props) {
  function logout() {
    props.auth.logOut()
  }

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Welcome to WellLine {props.auth.getCachedUser().profile.name} ({props.auth.getCachedUser().profile.unique_name})
        </p>
        <button onClick={logout}>
          Log Out
        </button>
        <p>
          Edit <code>src/App.js</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;
