 param (

    [string]$samaccountname
    
 )


 $Properties = "DisplayName", "EmployeeNumber", "HomeDirectory"  , "midas",  "loginshell" , "gidNumber", "uidNumber", "PasswordLastSet", "ProfilePath", "sAMAccountName", "LastBadPasswordAttempt", "extensionattribute1", "WhenCreated","lastLogon", "lastLogonTimestamp"

 

 If($samaccountname -ne ''){
 
    $this_user = Get-ADUser -Filter "sAMAccountName -eq '$samaccountname'" -Properties $Properties 
    
}else{

    Write-Host "No sAMAccountName entered, exiting...."
    exit


}

$output_array = @()

$output_array += $this_user | Select-Object $Properties
$output_array += $this_user | Select-Object @{n='ParentContainer';e={$_.distinguishedname -replace '^.+?,(CN|OU.+)','$1'}}
$output_array += $this_user | Select-Object @{N='LastLogon'; E={[DateTime]::FromFileTime($_.LastLogon)}}
$output_array += $this_user | Select-Object @{N='LastLogonTimestamp'; E={[DateTime]::FromFileTime($_.LastLogonTimestamp)}}

$output_array | Format-List