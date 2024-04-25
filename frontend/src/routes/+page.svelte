<script lang="ts">
    import {Toast} from '@skeletonlabs/skeleton';
    import { initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { onMount } from 'svelte';
    let sakrij = false
    async function proveriLogin() {
        try {
            
            const response = await fetch('http://localhost:5000/ulogovan', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }  
            });

            const data = await response.json();
            console.log(data);
            if(data['message']==='jeste')
            {
                sakrij = true;
            }
            else
                sakrij = false;
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
    proveriLogin()

</script>

{#if sakrij}
    <nav>
        <ul>
        <li><a href="/">Home</a></li>
        </ul>
    </nav>
{:else}
<nav>
    <ul>
      <li><a href="/">Home</a></li>
      <li><a href="/login">Login</a></li>
      <li><a href="/register">Register</a></li>
    </ul>
</nav>
{/if}

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
