<script>
    import {Toast} from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
</script>
<nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/login">Login</a></li>
      <li><a href="/register">Register</a></li>
    </ul>
</nav>
<div style="display: flex; justify-content:center; flex-direction:column">
    <h1>Welcome to Quiz!</h1>

</div>

<Toast></Toast>
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
</style>
