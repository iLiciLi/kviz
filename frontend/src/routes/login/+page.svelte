<script>
    let email = '';
    let password = '';
</script>

<nav>
    <ul>
        <li><a href="/">Home</a></li>
        <li><a href="/login">Login</a></li>
        <li><a href="/register">Register</a></li>
    </ul>
  </nav>

<div style="display: flex; justify-content:center; flex-direction:column">
    <h1>Please Log In.</h1>
    <form>
        <label for="email" class="selfc">Email:</label>
        <input type="email" id="email" class="selfc" bind:value={email} required/>

        <label for="password" class="selfc" >Password:</label>
        <input type="password" id="password" class="selfc" bind:value={password} required/>

        <button type="submit" class="selfc">Login</button>
    </form>
</div>
<style>
    *
    {
        text-align: center;
        display: block;
        margin: 2px;
        align-items: center;
        min-height: 50%;
    }
    :global(body)
    {
        height: 100vh;
        background: linear-gradient(to right, #1b5780, #504c52);
    }
    nav
    {
        padding: 10px;
        height:fit-content;
        min-height: 0%;
    }
    ul
    {
        display:flex;
        align-items: flex-end;
        justify-content: end;
    }
    li
    {
        display: inline;
    }

    a
    {
        color:black;
        text-decoration: none;
        font-weight: bold;
    }
    .selfc
    {
        align-self:center;
    }
    button
    {
        background-color: lightblue;
    }
</style>