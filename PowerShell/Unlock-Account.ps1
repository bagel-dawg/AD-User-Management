 param (
    [string]$samaccountname

    
 )

 $credentials = Get-Credential -Message "Enter credentials required for account unlock."

 Unlock-ADAccount $samaccountname  -Credential $credentials  -Confirm:$false 