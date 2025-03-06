from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer

class UserCreateSerializer(BaseUserCreateSerializer):
	class Meta(BaseUserCreateSerializer.Meta):
		fields = ['id', 'email', 'password']

	def create(self, validated_data):
		# Ensure email is used as username if needed
		validated_data["username"] = validated_data.get("email")
		return super().create(validated_data)