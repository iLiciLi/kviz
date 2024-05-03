<script lang="ts">
    import { AppShell, initializeStores, storeHighlightJs } from '@skeletonlabs/skeleton';
    initializeStores();
    import { goto } from '$app/navigation';
    import { getToastStore } from '@skeletonlabs/skeleton';
    import { Toast, type ToastSettings, type ToastStore } from '@skeletonlabs/skeleton';
    import {userID} from '$lib/stores.js';
    import { onMount,onDestroy } from 'svelte';

    const toastStore = getToastStore();

    let otpInput : String;
    let isLoggedIn : String | null;
    let uID : String | null;
    let sv = ''
    let mozeSlati = false

    onMount(()=>{ isLoggedIn = localStorage.getItem('isLoggedIn');uID = localStorage.getItem('userID')})

    async function saljiMail() {
        
        const formData = {
            uID
        };
        
        try {
            
            const response = await fetch('http://localhost:5000/saljiMail', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            console.log(data); // Handle response from backend
            if(data['messageEM'] === 'poslat mail')
            {
                mozeSlati = true
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }
    
    async function proveriV() {
        
        const formData = {
            uID
        };
        
        if(isLoggedIn==='true')
        {
            try {
                
                const response = await fetch('http://localhost:5000/proveriVerifikaciju', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(formData)
                });

                const data = await response.json();
                console.log(data); // Handle response from backend
                sv = data['messagePV']
                if(data['messagePV']==='nijeVerifikovan')
                {
                    saljiMail()
                }
                else if(data['messagePV'] === 'nijeUlogovan')
                {
                    goto('/login')
                }
                else if(data['messageV']==='verifikovan' || data['messagePV']==='jesteVerifikovan')
                {
                    sv = 'jesteVerifikovan';
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
        else
            sv = 'nijeLogovan';
        }

        


    async function verifikuj() {
        
        const formData = {
            uID,
            otpInput,
        };
        
        try {
            
            const response = await fetch('http://localhost:5000/verifikacija', {
                method: 'POST',
                credentials: 'include',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();
            console.log(data);
            if(data['messageV'] == 'verifikovan')
            {
                sv = 'jesteVerifikovan';
                const t: ToastSettings = {
	                message: data['messageV'],
                    timeout:2000,
                    background:'bg-primary-600',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
            }
            else
            {
                const t: ToastSettings = {
	                message: data['messageV'],
                    timeout:2000,
                    background:'bg-error-700',
                    hideDismiss: true,
                };
                toastStore.trigger(t);
            }
        } catch (error) {
            console.error('Error:', error);
        }
    }

    onMount(proveriV);
    

</script>


{#if sv === 'nijeVerifikovan'}
    <div style="display: flex; justify-content:center; flex-direction:column" class="h2">
        <h1 class="h1">VERIFIKACIJA!</h1>
        {#if mozeSlati === true}
            <form on:submit={verifikuj}>
                <label class="Label" for="vInput">OTP:</label>
                <input class="Input text-secondary-700" id='vInput' type="text" bind:value={otpInput}>
                <button class="btn variant-filled" type="submit">POTVRDI</button>
            </form>
        {:else}
            <h2>SALJE SE MAIL...</h2>
        {/if}
    </div>
{:else if sv === 'nijeLogovan'}
    <div style="display: flex; justify-content:center; flex-direction:column" class="h2">
        <h1>NISI ULOGOVAN, ULOGUJ SE DA BI MOGAO DA SE VERIFIKUJES</h1>
        <a class="btn variant-filled" href="/login">ULOGUJ SE</a>
    </div>
{:else}
    <div style="display: flex; justify-content:center; flex-direction:column" class="h2">
        <h1>VERIFIKOVAN SI</h1>
        <a class="btn variant-filled" href="/">Home</a>
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
    .h1
    {
        margin-bottom: 5%;
    }
</style>
