# Authentication/authorization

- RBAC (Role-based access control)
- ABAC (Attribute-based access control)

# Notes

- k8s cannot revoke certs
- when certificate is applied to the group of users (RBAC), a single user cannot be banned. to be able to ban particular user,
we should give him his own cert, create a personal rolebinding for him. and ban will look like editing his rolebindings.
this scheme looks not that good
