<script lang="ts">
    
    import { AppShell,initializeStores } from '@skeletonlabs/skeleton';
    initializeStores();
    import { getToastStore } from '@skeletonlabs/skeleton';
    import {Toast} from '@skeletonlabs/skeleton';
    import type { ToastSettings, ToastStore } from '@skeletonlabs/skeleton';
    import {userID} from '$lib/stores';
    import { onMount ,onDestroy} from 'svelte';

    let isLoggedIn : String | null;
    onMount(()=> isLoggedIn = localStorage.getItem('isLoggedIn'))


    const toastStore = getToastStore();

    let email = '';
    let password = '';
    let confirmPassword = '';

    
    import { goto } from '$app/navigation';
    async function submitForm() {
        
        // @ts-ignore
        document.getElementById('email').setAttribute("required","true");
        // @ts-ignore
        document.getElementById('password').setAttribute("required","true");
        // @ts-ignore
        document.getElementById('confirmPassword').setAttribute("required","true");
        
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
                    localStorage.setItem('isLoggedIn','true')
                    localStorage.setItem('userID',data['userAIDI'])
                    const t: ToastSettings = {
	                    message: data['message'],
                        classes: 'bg-primary-600',
                        timeout:2000,
                        hideDismiss: true,

                    };
                    toastStore.trigger(t);
                    setTimeout(() => {
                    if (data['message'] === 'Registration successful') 
                    {
                        goto('/verification');
                        }
                    }, 2500);
                }
                else
                {
                    const t: ToastSettings = {
	                    message: data['message'],
                        classes: 'bg-error-700',
                        timeout:2000,
                        hideDismiss: true,
                    };
                    toastStore.trigger(t);
                }
                
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
</script>


{#if isLoggedIn === 'false'}
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
            <input type="email" id="email" class="selfc" bind:value={email}/>

            <label for="password" class="selfc" >Password:</label>
            <input type="password" id="password" class="selfc" bind:value={password}/>

            <label for="confirmPassword" class="selfc" >Confirm Password:</label>
            <input type="password" id="confirmPassword" class="selfc" bind:value={confirmPassword}/>

            <button id='registerDugme' type="submit" class="selfc">Register</button>
        </form>
    </div>
{:else}
    <div style="display: flex; justify-content:center; flex-direction:column">
        <h1>VEC SI ULOGOVAN, VRATI SE NA POCETNU</h1>
        <li><a href="/">Home</a></li>
    </div>
{/if}
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