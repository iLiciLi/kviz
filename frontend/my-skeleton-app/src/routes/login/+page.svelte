<script lang="ts">
    let email = '';
    let password = '';
    import { AppShell, initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { goto } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { Toast, type ToastSettings, type ToastStore } from '@skeletonlabs/skeleton';
    const toastStore = getToastStore();

    async function submitFormLogin() {
        

        const formData = {
            email,
            password
        };

        try {
            
            const response = await fetch('http://localhost:5000/login', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            console.log(data); // Handle response from backend
            if(data['message']==='Incorrect email')
            {
                goto('/register');
            }
            if(data['message']==='Login successful')
            {
                const t: ToastSettings = {
	                message: data['message'],
                    timeout:2000,
                    background:'bg-primary-600',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
                //goto('/')
            }
            else
            {
                const t: ToastSettings = {
	                message: data['message'],
                    timeout:2000,
                    background: 'bg-error-700',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
            }
            
        } catch (error) {
            console.error('Error:', error);
        }
    }
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
    <form on:submit={submitFormLogin}>
        <label for="email" class="selfc">Email:</label>
        <input type="email" id="email" class="selfc" bind:value={email} required/>

        <label for="password" class="selfc" >Password:</label>
        <input type="password" id="password" class="selfc" bind:value={password} required/>

        <button type="submit" class="selfc">Login</button>
    </form>
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
    .selfc
    {
        align-self:center;
    }
    button
    {
        background-color: lightblue;
    }
</style>