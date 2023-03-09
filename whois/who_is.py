import whois

# Open th file containing the list of domain names that need to be looked up
with open("url_list") as file:

    # Use a loop to grab each line in the file
    for line in file:

        # remove whitespace from the domain name
        line = line.strip()

        # Make a query to whois
        w = whois.whois(url=line)

        # Open the file that will be written to, 'a' is used to append to the file and not overwrite it.
        with open("domain_info", "a") as write_file:

            # Set all the info to be obtained as variables
            city = w["city"]
            state = w["state"]
            status = w["status"]
            name = w["domain_name"]
            registrar = w["registrar"]
            # Loop through names if multiple were found, otherwise just write the name
            if name == None:
                write_file.write("Domain name not found \n\n\n")
                continue
            if type(name) == list:
                for line in name:
                    write_file.write(f"Domain Name: {line}\n")
            else:
                write_file.write(f"Domain Name: {name}\n")

            # Loop through status  if a list, otherwise just write the status
            if type(status) == list:
                for line in status:
                    write_file.write(f"Domain Status: {line}\n")
            else:
                write_file.write(f"Domain Status: {status}\n")

            # Write the registrar, city, and state to the file
            write_file.write(f"Registrar: {registrar}\n")
            write_file.write(f"City: {city}\n")
            write_file.write(f"State: {state}\n\n\n")
