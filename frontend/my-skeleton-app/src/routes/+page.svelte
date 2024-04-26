<script lang="ts">
    import { AppShell, initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { goto } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { Toast, type ToastSettings, type ToastStore } from '@skeletonlabs/skeleton';
    const toastStore = getToastStore();
    let sakrij = false
    let logoutDugme = false
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
                logoutDugme = true;
            }
            else
            {
                sakrij = false;
                logoutDugme = false;
            }
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
    proveriLogin()
    async function logoutUser() {
        try {
            
            const response = await fetch('http://localhost:5000/logout', {
                method: 'GET',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                }  
            });

            const data = await response.json();
            console.log(data);
            if(data['message']==='izlogovan')
            {
                sakrij = false;
                logoutDugme = false;
                goto('/')
                const t: ToastSettings = {
	                message: data['message'],
                    timeout:2000,
                    background:'bg-primary-600',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
            }
            else
            {
                sakrij = true;
                logoutDugme = true;
                const t: ToastSettings = {
	                message: 'Ulogovani ste',
                    timeout:2000,
                    background:'bg-primary-600',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
            }
            
        } catch (error) {
            console.error('Error:', error);
        }
    }

</script>

{#if sakrij}
    <nav>
        <ul>
        <li><a href="/">Home</a></li>
        <li><a id='logoutA' on:click={logoutUser} href="/">Logout</a></li>
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
