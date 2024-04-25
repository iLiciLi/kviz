<script lang="ts">
    import { AppShell,initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { getToastStore } from '@skeletonlabs/skeleton';
    import {Toast} from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    const toastStore = getToastStore();

    let email = '';
    let password = '';
    let confirmPassword = '';
    
    import { goto } from '$app/navigation';
    async function submitForm() {
        const formData = {
            email,
            password,
            confirmPassword
        };

        try {
            if (password === confirmPassword) {
                const response = await fetch('http://localhost:5000/register', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                console.log(data);
                if(data['message']==='Registration successful')
                {
                    const t: ToastSettings = {
	                    message: data['message'],
                        background: 'green',
                        //timeout:2000,
                        hideDismiss: true

                    };
                    toastStore.trigger(t);
                    goto('/')
                }
                else
                {
                    const t: ToastSettings = {
	                    message: data['message'],
                        background: 'yellow',
                        //timeout:2000,
                        hideDismiss: true
                    };
                    toastStore.trigger(t);
                }
                
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
    <h1>Please Register!</h1>
    <form id='registerForm' on:submit={submitForm}>
        <label for="email" class="selfc">Email:</label>
        <input type="email" id="email" class="selfc" bind:value={email} required/>

        <label for="password" class="selfc" >Password:</label>
        <input type="password" id="password" class="selfc" bind:value={password} required/>

        <label for="confirmPassword" class="selfc" >Confirm Password:</label>
        <input type="password" id="password" class="selfc" bind:value={confirmPassword} required/>

        <button id='registerDugme' type="submit" class="selfc">Register</button>
    </form>
</div>

<div class="bg-primary-500 text-secondary-500">
    <Toast></Toast>
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